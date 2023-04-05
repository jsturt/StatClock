import statclock as st
import matplotlib.pyplot as plt

data = st.initialize('nine inch whales','testdata.txt')

kdr = st.kd(data)
streak = st.killstreaks(data)
stddev = st.stdKills(data)

print("k/d : "+str(kdr)+" plus minus " + str(round(stddev,2)))

plt.hist(streak,bins=[i for i in range(max(streak)+2)],color='c',align='left')
plt.axvline(kdr,0,1,label='k/d',linestyle='--')
plt.axvline(kdr+stddev,0,1,label='k/d$\pm\sigma$',linestyle=':',color='r')
plt.axvline(kdr-stddev,0,1,linestyle=':',color='r')
plt.legend()
plt.xlabel('killstreak')
plt.ylabel('frequency')
plt.show()

