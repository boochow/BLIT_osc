import numpy as np
import matplotlib.pyplot as plt

def rgb(i):
    b = (i & 4) >> 2
    g = (i & 2) >> 1
    r = i & 1
    return (r, g, b)

colors = list(map(rgb, [1, 2, 4, 3, 5, 6]))

table_size = 512 # for a single wave
min_phi = 0.5 # plot from 0.5pi
max_phi = 2.5 # to 2.5pi

t = np.linspace(min_phi, max_phi, table_size, endpoint=False)
t += max_phi / table_size

max_harmonics = [50, 23, 7, 4, 3, 2, 1]
harmonics = list(map(lambda x: x * 2 + 1.0, max_harmonics))

# denominator part of SincM

plt.plot(t, 1. / np.sin(np.pi * t), color=colors[0], linewidth=1.0)
plt.xlabel('t')
plt.ylabel("$1 / \sin(x)$", fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5],["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.ylim(-10, 10)
plt.grid(True)
plt.show()

# numerator part of SincM

for i in range(4, len(max_harmonics)):
    plt.plot(t, np.sin(np.pi * harmonics[i] * t), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel("$\sin(nx)$", fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5], ["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.grid(True)
plt.show()


# generate SincM wavetables

wave_tables = []

# period: num of samples per wave
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

# SincM

for i in range(4, len(wave_tables)):
    plt.plot(t, wave_tables[i], color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel('$Sinc_{M}(x)$', fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5],["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.grid(True)
plt.show()

# normalised SincM

for i in range(0, len(wave_tables)):
    plt.plot(t, wave_tables[i] / harmonics[i], color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend()
plt.xlabel('t')
plt.ylabel('$Sinc_{M}(x)$, normalised', fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5],["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.grid(True)
plt.show()

# Integrated SincM

for i in range(0, len(wave_tables)):
    plt.plot(t, np.cumsum(wave_tables[i]), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend(loc="lower right")
plt.xlabel('t')
plt.ylabel('$\int Sinc_{M}(x)$', fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5],["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.grid(True)
plt.show()

# Integrated (SincM - constant)

average = 1. / period
for i in range(0, len(wave_tables)):
    plt.plot(t, np.cumsum(wave_tables[i] - average), color=colors[i % 6], linewidth=1.0, label='n='+str(max_harmonics[i]))

plt.legend(loc="lower right")
plt.xlabel('t')
plt.ylabel('$\int Sinc_m(x) - kx$', fontsize=16)
plt.xlim(min_phi, max_phi)
plt.xticks([0.5, 1, 1.5, 2, 2.5],["0.5$\phi$", "$\phi$", "1.5$\phi$", "2$\phi$", "2.5$\phi$"])
plt.ylim(-1.2, 1.2)
plt.grid(True)
plt.show()
