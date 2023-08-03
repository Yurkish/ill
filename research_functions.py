from functions import *
def import_csv_weather(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=';')
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), int(rowincsv["ts"]) // 1000, rowincsv["Temperature"]]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
    return data
def pearson_correlation_research(month_code,room,save_fig):
    print(' -> ',month_code, ' ', room)
    match month_code:
        case 'june':
            dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
            time_point_amount = 14320
            research_amount = 1000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop  = data[-1][1]
        case 'july':
            dataweather = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
            time_point_amount = 18720
            research_amount = 1000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop  = data[-1][1]
        case 'aug1':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 15000
            research_amount = 1000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
            time_start = 1596445120
            time_stop = 1597524902
        case 'aug2':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 14400
            research_amount = 1000
            time_point_amount = 15000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
            time_start = 1597613321
            time_stop  = 1598591287

    x = []
    y = []
    for row in data:
        if row[1] > time_stop:
            break
        elif row[1] < time_start:
            continue
        else:
            x.append(float(row[1]))
            y.append(float(row[2]))
    #########################################################################
    ### new time points net ###########
    time_new = np.linspace(x[0], x[-1], num=time_point_amount, endpoint=True)
    tt = np.linspace(0, (x[-1] - x[0]), num=time_point_amount, endpoint=True)
    t_days = tt/86400

    #########################################################################
    ### interpolated function of temperature inside the room ################
    r_t = interp1d(x, y, kind='linear')
    #########################################################################
    # here we get data from meteostation dataset
    # time of measurement matches with time point for interpolation
    #
    ind = 1
    indd = 0
    w = np.zeros(time_point_amount)
    room_inter = np.zeros(time_point_amount)
    fin = int(dataweather[-1][0])
    for row in time_new:
        time_is_now = float(row)
        for i in range(ind, fin):
            if int(dataweather[i][1]) < time_is_now:
                continue
            else:
                ind = i
                break
        w[indd] = "%.7f" % float(dataweather[ind][2])
        room_inter[indd] = "%.7f" % float(r_t(time_is_now))
        indd += 1
    #cs = CubicSpline(x, y)

    # for k in kind_lst:
    #     f = interp1d(x, y, kind=k)
    #     y_new = f(x_new)
    #     plt.plot(x_new, y_new, label=k)

    # R = len(x)
    # print('\n R = ',R, '\n')
    # for row in range(R):
    #     diff1 = cs(x[row]) - y[row]
    #     diff2 = y[row] - room_funct(x[row])
    #     print('d[2] = ', data[row][2], 'y=',y[row] ,' cs=', cs(data[row][1]),' diff1 = ', diff1 ,' diff2 = ', diff2 ,'\n')
    #########################################################
    ##### here we start our estimation research #############
    #########################################################
    ratio = 0.7
    w1 = dividing_lists(w, ratio)
    room_inter1 = dividing_lists(room_inter, ratio)
    room_weather_corr = np.corrcoef(room_inter1[0], w1[0])
    print('room_weather_corr')
    print (room_weather_corr)
    #########################################################
    ##### creating file for research results ################
    #########################################################
    research_file_name = 'SHIFT SEARCH ' + month_code + ' ' + room + '.csv'

    #########################################################
    ##### let's shift reading frame #########################
    #########################################################
    search_for_maximum_corr = np.zeros(research_amount)
    #
    w_reduced = w[:time_point_amount - research_amount]

    with open(research_file_name, 'w', newline='') as research_res_file:
        conc = csv.DictWriter(research_res_file, delimiter=";", fieldnames=['step', 'ts', 'tm', 'pearson'])
        conc.writeheader()
        for i in range(research_amount):
         # room temperature with i-shifted frame
            room_research = room_inter[i:time_point_amount - research_amount + i]
        # correlation of shifted room-t frame and fixed weather-t frame
            search_for_maximum_corr[i] = np.corrcoef(room_research, w_reduced)[0][1]
            #print(i,' -> PC for ', int(i*(time_stop-time_start)/(time_point_amount*60)), ' min. = ', search_for_maximum_corr [i])
            t_s = int(i*(time_stop-time_start)/(time_point_amount))
            t_m = i*(time_stop-time_start)/(time_point_amount*60)
            conc.writerow(dict(step="%.d" % i, ts="%.d" % t_s, tm="%.1f" % t_m, pearson="%.3f" % search_for_maximum_corr [i]))
    research_res_file.close()
    print(np.where(search_for_maximum_corr == max(search_for_maximum_corr)))
    print(np.argmax(search_for_maximum_corr))
    ########################################################
    ### best for correlation shift size ####################
    chosen_shift = np.argmax(search_for_maximum_corr)
    room_shifted = room_inter[chosen_shift:time_point_amount - research_amount + chosen_shift]

    ###################################################
    slope, intercept, r, p, std_err = stats.linregress(w_reduced, room_shifted)
    old_res = stats.linregress(w_reduced, room_inter[:time_point_amount - research_amount])
    print('r-old = ', old_res.rvalue, ', r-new = ', r)
    print('slope = ', slope, ', intercept = ', intercept, ', std_err =', std_err)
    #########################################################################
    ### prediction of room_temperature from shifted weather temp ############
    def linear_room_weather_prediction(x):
        return slope * x + intercept
    #########################################################################
    ###### prepareing predicting array ######################################
    mymodel = list(map(linear_room_weather_prediction, w_reduced))
    linear_deviation = np.std(mymodel - room_shifted)
    print('std_deviation = ', linear_deviation)
    #########################################################################
    figure_shifting, (initial_fig, correl_to_shift, shifted_fig) = plt.subplots(3, 1, constrained_layout=True)
    # initial_fig.plot(time_new, room_inter,'-')
    # initial_fig.plot(time_new, w, '-.')
    initial_fig.plot(t_days, room_inter,'-')
    initial_fig.plot(t_days, w, '-')
    initial_fig.set_title('Initial data')
    initial_fig.set_xlabel('Days')
    initial_fig.set_ylabel('temperature (C)')
    y_inf = min(w)
    y_sup = max(w)
    initial_fig.set_ylim([y_inf,y_sup])

    correl_to_shift.plot(tt[:research_amount],search_for_maximum_corr,'-')
    #correl_to_shift.plot(tt,w/max(w), '-')
    correl_to_shift.set_xlabel('time (S)')
    correl_to_shift.set_title('shifting ' + str(chosen_shift*(time_stop-time_start)/(time_point_amount*3600)) + ' hours')
    #correl_to_shift.set_xlim([0,500])
    correl_to_shift.set_ylim([0, 1])
    correl_to_shift.axhline(y=max(search_for_maximum_corr), color='r', linestyle='dashdot')
    correl_to_shift.axvline(x=tt[chosen_shift], color='r', linestyle='dashdot')
    correl_to_shift.axvline(x=tt[0], color='r', linestyle='dashdot')
    #correl_to_shift.text(3, 8, 'boxed italics text in data coords', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    shifted_fig.plot(t_days[:time_point_amount - research_amount],w[:time_point_amount - research_amount],'-', t_days[:time_point_amount - research_amount],room_inter[chosen_shift:time_point_amount - research_amount+chosen_shift], t_days[:time_point_amount - research_amount],room_inter[:time_point_amount - research_amount], '-')
    shifted_fig.axvline(x=t_days[0], color='r', linestyle='dashdot')
    shifted_fig.axvline(x=1, color='r', linestyle='dashdot')
    shifted_fig.axvline(x=1+chosen_shift*(time_stop-time_start)/(time_point_amount*3600*24), color='r', linestyle='dashdot')
    shifted_fig.axvline(x=t_days[chosen_shift], color='r', linestyle='dashdot')
    shifted_fig.legend(['погода', 'комната сдвиг.', 'комната нач.'], loc='best')
    #shifted_fig.plot(tt[:research_amount],search_for_maximum_corr,'-')
    shifted_fig.set_xlabel('Дни')
    shifted_fig.set_title('Синхронизированные кривые')
    shifted_fig.set_ylim([y_inf,y_sup])
    figure_shifting.suptitle(month_code + ' ' + room, fontsize=16)
    # plt.show()
    #
    # plt.plot(x,y,'*',time_new, r_t(time_new),'-')
    # plt.legend(['raw','linear'], loc='best')
    #plt.show()
    if save_fig == 1:
        fig11 = plt.gcf()
        fig11.set_size_inches((13, 10), forward=False)
        fig11.savefig(month_code + ' ' + room, dpi = 500)

    time_of_shift = chosen_shift*(time_stop-time_start)/(time_point_amount*3600)
    vector_of_returns = [time_of_shift, chosen_shift, max(search_for_maximum_corr), time_start, time_stop, time_point_amount]
    return vector_of_returns

def research_funct(sens_code):
    match sens_code:
        case 1:
            sensorfilename = 'data/Vega Smart-UM 1VSm_383437315E396B0E_1.csv'
        case 2:
            sensorfilename = 'data/Vega Smart-UM 2VSm_383437315E396B0E_1.csv'
        case 3:
            sensorfilename = 'data/Vega Smart-UM 3VSm_383437315E396B0E_1.csv'
        case 4:
            sensorfilename = 'data/Vega Smart-UM 4VSm_383437315E396B0E_1.csv'

    print('File for research: ' + sensorfilename)
    s1 = import_csv_temperature(sensorfilename,';')
    s2 = import_csv_illumination(sensorfilename,';')
    time_temperature = []
    temperature = []
    time_illumination = []
    illumination = []

    for row in s1:
        time_temperature.append(row[1])
        temperature.append(row[2])
    for row in s2:
        time_illumination.append(row[1])
        if row[2] < 4000:
            illumination.append(row[2])
        else:
            illumination.append(0)
    time_point_amount = len(temperature)

    illumination_array = np.array(illumination)
    temperature_array = np.array(temperature)

    research_period = 70
    research_start = 2000
    research_end = 6000
    research_coeff = np.zeros(research_period)
    ind = np.zeros(research_period)
    for i in range(research_period):
        research_coeff[i]=np.corrcoef(illumination_array[research_start:research_end],temperature_array[research_start+i:research_end+i])[0][1]
        ind[i] = i*5

    plot_array(range(research_end-research_start),illumination_array[research_start:research_end])
    plot_array_minutes(ind,research_coeff)
    return 0
