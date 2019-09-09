from datetime import datetime,timedelta
import time


def datelist(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    print(start_date)
    end_date = datetime.strptime(end, "%Y-%m-%d")
    result = []
    curr_date = start_date
    while curr_date != end_date:
        # result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        result.append(curr_date.strftime("%Y-%m-%d"))
        curr_date += timedelta(1)
    # result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    result.append(curr_date.strftime("%Y-%m-%d"))
    return result


if __name__ == "__main__":
    datelist("2016-06-07", "2016-06-27")
