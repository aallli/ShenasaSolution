from jalali_date import datetime2jalali


def to_jalali_full(date):
    return datetime2jalali(date).strftime('%H:%M:%S %y/%m/%d')