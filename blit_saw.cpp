/*
 * File: blit_saw.cpp
 * a BLIT based sawtooth oscillator 
 */

#include <math.h>
#include "userosc.h"

#define MIN_PHI 0.f
#define MAX_PHI 2.f
#define MIN_LEAK 0.9999f
#define MAX_VOL 0.8

typedef struct State {
    float phi;
    float leaky;
    float sig;
    uint16_t freq_max;
    uint16_t harmonics_max;
    uint8_t flags;
} State;

enum {
    k_flags_none = 0,
    k_flag_reset = 1<<0,
};

static State s_osc;
static bool sincm = false;

void OSC_INIT(uint32_t platform, uint32_t api)
{
    s_osc.phi = 0.5;
    s_osc.leaky = MIN_LEAK;
    s_osc.sig = 0.f;
    s_osc.freq_max = k_samplerate / 2;
    s_osc.flags = k_flags_none;
}

void OSC_CYCLE(const user_osc_param_t * const params,
               int32_t *yn,
               const uint32_t frames)
{
    const uint8_t flags = s_osc.flags;
    s_osc.flags = k_flags_none;
    
    const float note = (params->pitch >> 8) + (params->pitch & 0xFF)/256.0f;
    const float w0 = osc_w0f_for_note((params->pitch) >> 8, params->pitch & 0xFF);
    const float freq = osc_notehzf(note);
    const int n_harmonics = clipmaxi32(int(s_osc.freq_max / freq), s_osc.harmonics_max) - 1;
    const int m_for_sincm = 2 * n_harmonics + 1;
    const float period = 1.f * k_samplerate / freq / 2;
    const float average = 1.f / period;

    float phi = (flags & k_flag_reset) ? 0.5f : s_osc.phi;
    float sig = (flags & k_flag_reset) ? 0.f : s_osc.sig;
    float leaky = s_osc.leaky;

    q31_t * __restrict y = (q31_t *) yn;
    const q31_t * y_e = y + frames;
    
    for (; y != y_e; ) {
        float sinc_d = sinf(M_PI * phi);

        float phi_n = phi * m_for_sincm;
        phi_n -= int(phi_n) / 2 * 2;
        float sinc_n = sinf(M_PI * phi_n);

        float sinc_m;
        if (fabs(sinc_d) < 1.e-5) {
            sinc_m = (float) m_for_sincm / period;
        } else {
            sinc_m = sinc_n / sinc_d / period;
        }

        sig = sig * leaky + sinc_m - average;
        if (sincm) {
            *(y++) = f32_to_q31(sinc_m);
        } else {
            *(y++) = f32_to_q31(sig * MAX_VOL);
        }

        phi += w0;
        if (phi > MAX_PHI) {
            phi -= MAX_PHI;
        }
    }
    s_osc.phi = phi;
    s_osc.sig = sig;
}

void OSC_NOTEON(const user_osc_param_t * const params)
{
    s_osc.flags |= k_flag_reset;
}

void OSC_NOTEOFF(const user_osc_param_t * const params)
{
    (void) params;
}

void OSC_PARAM(uint16_t index, uint16_t value)
{
    switch (index) {
    case k_user_osc_param_id1:
        s_osc.leaky = MIN_LEAK - 0.0001 * value;
        break;
    case k_user_osc_param_id2:
        s_osc.freq_max = k_samplerate / 2 * (1.0 - 0.009 * value);
        break;
    case k_user_osc_param_id3:
        if (value == 0) {
            s_osc.harmonics_max = 48000;
        } else {
            s_osc.harmonics_max = value;
        }
        break;
    case k_user_osc_param_id4:
        if (value == 0) {
            sincm = false;
        } else {
            sincm = true;
        }
    default:
        break;
  }
}
