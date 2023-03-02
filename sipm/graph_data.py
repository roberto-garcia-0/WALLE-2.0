import matplotlib.pyplot as plt

m_s = {}
data0 = []
data4 = []
fn = open("/home/ebony/Documents/WALLE-2.0/sipm/temp_samples/sample_3.txt","r")
for line in fn:
     #print(len(line.split()))
    # m, s, one, four = line.split(' ')
    data = line.split()
    if (int(data[0]), int(data[1])) not in m_s:
        m_s[(int(data[0]), int(data[1]))] = 1
    else:
        m_s[(int(data[0]), int(data[1]))] += 1
    data0.append(float(data[2]))
    data4.append(float(data[3]))


print(m_s.values())
print(min(m_s.values()))
print(max(m_s.values()))

# plt.title("voltage graph of data 0, input: high")
# plt.xlabel('time domain, max time 1 min')
# plt.ylabel('Voltage (out of 5V')
# # plt.yticks(data0)
# plt.plot(data0)
  
# plt.savefig('/home/ebony/Documents/WALLE-2.0/sipm/temp_samples/test1_high.png')
# plt.show()

#how many samples per sec
