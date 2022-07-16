import numpy as np
import matplotlib.pyplot as plt

table_size = 512 # for a single wave
min_phi = 0.5 # plot from 0.5pi
max_phi = 2.5 # to 2.5pi

max_harmonics = [50, 23, 7, 4, 3, 2, 1]
harmonics = list(map(lambda x: x * 2 + 1.0, max_harmonics))

# generate blit wavetables

t = np.linspace(min_phi, max_phi, table_size, endpoint=False)
t += max_phi / table_size

wave_tables = []

# period: num of samples per 2pi
period = table_size / (max_phi - min_phi) / 2

# blit = (M/P) * sincM( (M/P) * n ), sincM(x) = sin(x) / (M * sin(x / M))
# blit = (M/P) * sin(pi * x * M / P) * (1/M) / sin(pi *x * M / P / M)
#      = (1/P) * sin(pi * x * M / P) / sin(pi * x / P)
# t = x/P
# blit = sin(pi * t * M) / sin(pi * t) / P

for h in harmonics:
    wt = np.zeros(shape = (t.shape[0],),)
    wt += np.sin(np.pi * h * t) / np.sin(np.pi * t) / period
    wave_tables.append(wt)

# plot waveforms

def rgb(i):
    b = (i & 4) >> 2
    g = (i & 2) >> 1
    r = i & 1
    return (r, g, b)

colors = list(map(rgb, [1, 2, 4, 3, 5, 6]))

# denominator part of SincM

plt.plot(t, 1. / np.sin(np.pi * t), color=colors[0], linewidth=1.0)
plt.xlabel('t')
plt.ylabel('1 / sin(x)')
plt.xlim(min_phi, max_phi)
plt.ylim(-10, 10)
plt.grid(True)
plt.show()

# numerator part of SincM

for i in range(4, len(wave_tables)):
#    plt.plot(t, wave_tables[i] * np.sin(np.pi * t), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))
    plt.plot(t, np.sin(np.pi * harmonics[i] * t), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel('sin(nx)')
plt.xlim(min_phi, max_phi)
plt.grid(True)
plt.show()

# SincM

for i in range(4, len(wave_tables)):
    plt.plot(t, wave_tables[i], color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel('Sinc_m(x)')
plt.xlim(min_phi, max_phi)
plt.grid(True)
plt.show()

# normalised SincM

for i in range(0, len(wave_tables)):
    plt.plot(t, wave_tables[i] / harmonics[i], color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel('Sinc_m(x), normalised')
plt.xlim(min_phi, max_phi)
plt.grid(True)
plt.show()

# Integrated SincM

for i in range(0, len(wave_tables)):
    plt.plot(t, np.cumsum(wave_tables[i]), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend(loc="lower right")
plt.xlabel('t')
plt.ylabel('Integral(Sinc_m(x))')
plt.xlim(min_phi, max_phi)
plt.grid(True)
plt.show()

# Integrated (SincM - constant)

average = 1. / period
for i in range(0, len(wave_tables)):
    plt.plot(t, np.cumsum(wave_tables[i] - average), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend(loc="lower right")
plt.xlabel('t')
plt.ylabel('Integral(Sinc_m(x) - kx)')
plt.xlim(min_phi, max_phi)
plt.ylim(-1.2, 1.2)
plt.grid(True)
plt.show()
