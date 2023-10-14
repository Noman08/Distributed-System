import matplotlib.pyplot as plt

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()

x_axis = "Servers"
y_axis = "Consistency delay"

servers = [1,2,3,4,5,6,7,8]

times_lab3_before_segmentation = [40,41,41,41,41,41,41,41]

times_lab3_after_segmentation = [30,31,30,30,31,30,30,30]

times_lab2 = [100,100,96,102,100,100,101,100]


plt.plot(servers, times_lab3_before_segmentation)
plt.plot(servers, times_lab2)
plt.plot(servers, times_lab3_after_segmentation)
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.legend(["task-A-no-segmentation", "lab2","with segmentation"])
plt.show()
