import numpy as np
import matplotlib.pyplot as plt

table_size = 512 # for a half wave
min_phi = 0.5
max_phi = 60.

max_harmonics = [17, 16]
harmonics = list(map(float, max_harmonics))

# generate wavetables

t = np.linspace(min_phi, max_phi, table_size, endpoint=False)
t += max_phi / table_size / 2

wave_tables = []

for m in harmonics:
    wt = np.zeros(shape = (t.shape[0],),)
    wt += np.sin(np.pi * t) / (m * np.sin(np.pi * t / m))
    wave_tables.append(wt)

# plot waveforms

def rgb(i):
    b = (i & 4) >> 2
    g = (i & 2) >> 1
    r = i & 1
    return (r, g, b)

colors = list(map(rgb, [1, 2, 4, 3, 5, 6]))

for i in range(0, len(wave_tables)):
    plt.plot(t, wave_tables[i], color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend(loc="lower center")
plt.xlabel('t')
plt.ylabel('x(t)')
plt.xlim(min_phi, max_phi)
plt.grid(True)
plt.show()
