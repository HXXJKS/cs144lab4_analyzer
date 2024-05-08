import numpy as np
import matplotlib.pyplot as plt

with open('data.txt', 'r') as source_file:

    # read the first line off
    source_file.readline()

    # var
    recevied_cnt = 0
    total_cnt = 0

    # consecutive
    consec_cnt = 0
    tmp_consec = 0

    # non-consecutive
    noncon_cnt = 0
    tmp_non_con = 0

    # pack loss
    receive_to_not = 0
    not_to_receive = 0

    # RTT
    minRtt = 0
    maxRtt = 0

    # plotting containers
    x_vals = []
    y_vals = []

    for line in source_file:
        icmp_seq_index = line.find('icmp_seq=')
        ttl_index = line.find(' ttl=')
        time_index = line.find('time=')

        # Extract the values of icmp_seq and ttl using string slicing
        icmp_seq = int(line[icmp_seq_index + len('icmp_seq='):ttl_index])
        ttl = int(line[ttl_index + len(' ttl='):].split()[0])
        time_value = int(line[time_index + len('time='):].split()[0])

        x_vals.append(icmp_seq * 0.2)
        y_vals.append(time_value)

        if minRtt == 0:
            minRtt = time_value

        if maxRtt < time_value:
            maxRtt = time_value

        if minRtt > time_value:
            minRtt = time_value

        # consecutive
        if (icmp_seq == total_cnt + 1):
            if tmp_non_con > 0:
                tmp_non_con = 0
                not_to_receive += 1
            tmp_consec += 1
            if tmp_consec > consec_cnt:
                consec_cnt = tmp_consec
        else:  # non consec
            if tmp_consec > 0:
                tmp_consec = 0
                receive_to_not += 1
            tmp_non_con += 1
            if tmp_non_con > noncon_cnt:
                noncon_cnt = tmp_non_con

        total_cnt = icmp_seq
        recevied_cnt += 1

    print("received cnt:", recevied_cnt)
    print("total sent cnt:", total_cnt)
    print("delivery rate:", recevied_cnt / total_cnt)
    print("largest consecutive:", consec_cnt)
    print("largest non consec:", noncon_cnt)
    print("r to r:", (recevied_cnt - receive_to_not) / recevied_cnt)
    print("n to r:", not_to_receive / (total_cnt - recevied_cnt))
    print("minRTT:", minRtt)
    print("maxRTT:", maxRtt)

    plt.plot(x_vals, y_vals)

    # Add labels and title
    plt.xlabel('time (sec)')
    plt.ylabel('RTT (ms)')
    plt.title('RTT vs time')

    # Display the graph
    plt.savefig('plot.png')

    plt.clf()

    # histogram
    plt.hist([x_vals, y_vals], bins=5, label=['time (sec)', 'RTT (ms)'])

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Two Containers')

    # Add legend
    plt.legend()

    # Display the histogram
    plt.savefig('histogram.png')

    plt.clf()

    # correlation
    x_cor = [x - y_vals[0] for x in y_vals]
    y_cor = [x - y_vals[1] for x in y_vals]

    corr_coef = np.corrcoef(x_cor, y_cor)[0, 1]
    plt.scatter(x_cor, y_cor)

    # Add labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Correlation Graph')

    # Add correlation coefficient as text on the plot
    plt.text(
        1, 8, f'Correlation coefficient: {corr_coef:.2f}', fontsize=10, color='red')

    # Display the plot
    plt.savefig('correlation.png')
