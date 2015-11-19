'''
Created on 2011-1-20

@author: michael

'''

import commonutils as cu
import xml.dom.minidom as mdom
import xlrd, re, datetime
import contractutils

__cal__ = contractutils.ContractCalculator();
__cal__.buildValueTable("ABBN", 90, 99.99);
__cal__.buildValueTable("AXT", 90, 99.995);
__cal__.buildValueTable("AYT", 90, 99.995);



__exchange_alias__ = [
    ['SFE', 'SFE.*'],
    ['CBT', 'CBOT'],
    ['CME', 'CME.*'],
    ['EUR', 'EURX', 'Eurex-D', 'ENXTFUT-D'],
    ['SGX', 'SGX.*'],
    ['Liffe', 'NYSE.*', 'MONP']              
]

__exchange_open_time__ = {
'SFE': {'day': '00:00:00-16:32:00', 'day_other': '16:58:00-23:59:59', 'offset':-1, 'TZ':'Australia/Sydney'},
'CME': {'day': '00:00:00-16:32:59', 'day_other': '16:58:00-23:59:59', 'offset':-1, 'TZ': 'America/Chicago'},
'CBT': {'day': '00:00:00-16:32:59', 'day_other': '16:58:00-23:59:59', 'offset':-1, 'TZ': 'America/Chicago'},
'EUR': {'day': '8:58:00-23:59:59', 'day_other': '00:00:00-8:02:00', 'offset':1, 'TZ': 'Europe/Berlin'},
'Liffe': {'day': '6:58:00-23:59:59', 'day_other': '00:00:00-06:02:00', 'offset':1, 'TZ': 'Europe/London'},
'SGX': {'day': '6:58:00-23:59:59', 'day_other': '00:00:00-06:02:00', 'offset':1, 'TZ': 'Asia/Singapore'}                          
}

__product_alias__ = [
    ['ABBN', 'SFE IR', 'IR \d{4}', 'IRU1', 'IR.\d'],
    ['AYT', 'SFE YT', 'YT \d{4}', 'YT.\d'],
    ['AXT', 'SFE XT', 'XT \d{4}', 'XT.\d'],
    ['TN1', 'ZN'],
    ['ASPI', 'SFE AP', 'AP \d{4}', 'AP.\d'],
    ['FCE', 'jFCE'],
    ['CES', 'ES'],
    ['NZTB', 'NZFOE BB'],
    ['CAU', '6A'],
    ['NCO', 'CL'],
    ['CJY', '6J'],
    ['STW', 'TW'],
    ['SNK', 'NK'],
    ['EFDX', 'FDAX'],
    ['CEC', '6E'],
    ['SJB', 'JB'],
    ['SIBC','SFE IB'],
    ['EUR', 'GE']
]

__product_tick_multiplier__ = {

'ABBN': {'tick': 24, 'multiplier': 100, 'commission': 1},
'AYT': {'tick': 28, 'multiplier': 100, 'commission': 1},
'AXT': {'tick': 8, 'multiplier': 1000, 'commission': 1},
'ASPI': {'tick': 25, 'multiplier': 1, 'commission': 1},
'EFDX': {'tick': 2.5, 'multiplier': 10, 'commission': 0.60},
'FESX': {'tick': 10, 'multiplier': 1, 'commission': 0.40},
'FCE': {'tick': 1, 'multiplier': 10, 'commission': 0.37},
'CES': {'tick': 0.5, 'multiplier': 100, 'commission': 0.61},
'TN1': {'tick': 1, 'multiplier': 1000, 'commission': 0.56},
'CCN': {'tick': 0.5, 'multiplier': 100, 'commission': 0.56},
'CSB': {'tick': 0.5, 'multiplier': 100, 'commission': 0.56},
'CSM': {'tick': 10, 'multiplier': 10, 'commission': 0.56},
'CSO': {'tick': 6, 'multiplier': 100, 'commission': 0.56},
'CWH': {'tick': 0.5, 'multiplier': 100, 'commission': 0.56},
'CAU': {'tick': 10, 'multiplier': 100, 'commission': 0.61},
'CJY': {'tick': 12.5, 'multiplier': 100, 'commission': 0.61},
'CEC': {'tick': 12.5, 'multiplier': 10000, 'commission': 0.61},
'NCO': {'tick': 10, 'multiplier': 100, 'commission': 1.58},
'SNK': {'tick': 500, 'multiplier': 1, 'commission': 0.95},
'STW': {'tick': 10, 'multiplier': 10, 'commission': 0.75},
'FGBL': {'tick': 10, 'multiplier': 100, 'commission': 0.30},
'FGBM': {'tick': 10, 'multiplier': 100, 'commission': 0.30},
'FGBS': {'tick': 1, 'multiplier': 1000, 'commission': 0.30},
'NZTB': {'tick': 24, 'multiplier': 100, 'commission': 1.0},
'SJB': {'tick': 1, 'multiplier': 100, 'commission': 1.0},
'SIBC': {'tick': 2.466, 'multiplier': 1000, 'commission': 1.0},
'EUR': {'tick': 2.5, 'multiplier': 1000, 'commission': 0.61},
'DEFAULT': {'tick': 0, 'multiplier': 0, 'commission': 0}
                                
}

def caculate_mfg_date(exchange, datetime_obj):
    ex = exchange;
    dt = datetime_obj;
    
    ex = get_standard_exchange_name(ex);
    
    # get the datetime object from timestamp
    ts_time = dt.time();
    ts_date = dt.date();
    
    # read the time table of the exchange
    tt = __exchange_open_time__[ex];
    day = tt['day'];
    day_other = tt['day_other'];
    offset = tt['offset'];
    
    # test current day
    times = day.split('-');
    b_time = datetime.datetime.strptime(times[0], '%H:%M:%S');
    e_time = datetime.datetime.strptime(times[1], '%H:%M:%S');
    b_time = b_time.time();
    e_time = e_time.time();
    if(ts_time >= b_time and ts_time <= e_time):
        date_str = ts_date.strftime('%Y%m%d');
         
        # deal with weekend
        if(ts_date.weekday() > 4):
            if(offset > 0):
                date_str = cu.last_work_day(date_str);
            else:
                date_str = cu.next_work_day(date_str);
        return date_str;
    
    # test the other day
    times = day_other.split('-');
    b_time = datetime.datetime.strptime(times[0], '%H:%M:%S');
    e_time = datetime.datetime.strptime(times[1], '%H:%M:%S');
    b_time = b_time.time();
    e_time = e_time.time();
    if(ts_time >= b_time and ts_time <= e_time):
        # get the offset
        date_str = ts_date.strftime('%Y%m%d');
        if(offset < 0):
            return cu.next_work_day(date_str);
        else:
            return cu.last_work_day(date_str);
    else:
        raise Exception('cannot determine the date for the trading record')
                               

def get_standard_product_name(name):
    for name_grp in __product_alias__:
        for pattern in name_grp:
            if(re.match(pattern, name)):
                return name_grp[0]
    return name;

def get_standard_exchange_name(name):
    for name_grp in __exchange_alias__:
        for pattern in name_grp:
            if(re.match(pattern, name)):
                return name_grp[0]
    return name;
                               
class OpenPosition(object):
    def __init__(self):
        self.account = None;
        self.product = None;
        self.quantity = 0;
        self.price = 0;
        self.date = None;
        pass
    
    
class TradeRecord(object):  
    def __init__(self):
        self.id = None;
        self.datetime = None;
        self.account = None;
        self.product = None;
        self.price = 0;
        self.quantity = 0;
        self.bought_sold = None; #bought/sold        
        self.exchange = None;
        self.currency = 'USD'; # by default
        self.fee_currency = 'USD';
        
        # used only for MFG records
        self.commission = 0;
        self.gst = 0;
        self.mfgdate = None;
        
        
        
    def __compareproduct__(self, other):   
        if(self.product == other.product):
            return True
        
        for name in __product_alias__:
            matchA = False;
            for pattern in name:
                if(re.match(pattern, self.product)):
                    matchA = True;
                    break;
            if(matchA is True):
                for pattern in name:
                    if(re.match(pattern, other.product)):
                        return True;        
        return False;
    
    def __eq__(self, other):
        if self is other:
            return True;
        if(self.id != other.id):
            return False;
        if(self.datetime != other.datetime):
            return False;
        
        # speical treatment for account
        if(self.account.upper()[0:6] != other.account.upper()[0:6]):
            return False;
        
        # for product
        if(self.__compareproduct__(other) is False):
            return False;
        
        
        if(self.price != other.price):
            return False;
        if(self.quantity != other.quantity):
            return False;
        if(self.bought_sold != other.bought_sold):
            return False;
        return True;        

class AccountProductSummary(object):
    def __init__(self):
        self.account = None;
        self.product = None;
        self.buy_qty = 0;
        self.sell_qty = 0;
        self.exchange = None;
        self.currency = None;
        self.fee_currency = None;
        # leave for future
        self.profit = 0;
        self.commission = 0;
        self.gst = 0;
        
        # used for open positions
        self.open_qty = 0;
        self.open_price = 0;


def parseXConnectPDF(fileName):
    cmd = "pdftohtml -xml -stdout %s" % fileName;
    (raw, err) = cu.run_cmd_get_output(cmd);
    if(err != ''):
        raise IOError;
    raw = raw.replace('\n', '');
    doc = mdom.parseString(raw);
    top = doc.documentElement;
    
    # 1. extract text from XML tags.
    pages = top.getElementsByTagName('page');
    lines = [];
    for page in pages:
        line_nodes = page.getElementsByTagName('b');
        for line_node in line_nodes:
            lines.append('/%s/' % line_node.firstChild.nodeValue);
    return lines;

def get_rts_trade_records(csv_file, from_ts=None, to_ts=None, enable_header=False):
    records = [];
    map = {
        'account': 2,
        'product': 0,
        'exchange':4,
        'bought_quantity': 11,
        'sold_quantity': 10,
        'price' : 14,
        'time': 7,
        'date': 6,
        'currency': 15         
    };
    
    # read raw data from file.
    file = open(csv_file, 'r');
    lines = file.readlines();
    file.close();
    
    for i in range(len(lines)):
        # deal with header
        if(i == 0 and enable_header):
            continue;
        
        fields = lines[i].split(',');
        # deal with time period
        timestamp = int(fields[map['time']]);
        if(from_ts is None):
            from_ts = 0;
        if(to_ts is None):
            to_ts = 240000;
        if(timestamp < from_ts or timestamp > to_ts):
            continue;
        
        record = TradeRecord();
        
        record.account = fields[map['account']].strip().strip('"');
        if(len(record.account) > 6):
            record.account = record.account[0:6];
        
        product = fields[map['product']].strip().strip('"');
        product = get_standard_product_name(product);
        record.product = product
        
        record.exchange = fields[map['exchange']].strip().strip('"');
        record.price = float(fields[map['price']].strip());
        record.currency = fields[map['currency']].strip().strip('"');
        
        # deal with bought sell and quantity
        b_qty = int(fields[map['bought_quantity']]);
        s_qty = int(fields[map['sold_quantity']]);
        if(b_qty != 0):
            record.bought_sold = 'B';
            record.quantity = abs(b_qty);
        else:
            record.bought_sold = 'S';
            record.quantity = abs(s_qty);
            
            
        # deal with date and time
        d = fields[map['date']].strip().strip('"');
        t = fields[map['time']].strip().strip('"');
        if(len(t) == 5):
            t = '0' + t;
        dt = d + t;
        #record.datetime = int(time.mktime(time.strptime(dt, '%Y%m%d%H%M%S')));
        
        record.datetime = datetime.datetime.strptime(dt, '%Y%m%d%H%M%S');
        
        
        records.append(record);
        
    return records;
        
def get_tt_trade_records(csv_file):
    records = [];
    map = {
        'account': 10,
        'bought_sold': 2,
        'quantity': 3,
        'exchange':1,
        'price' : 5,
        'product_type': 24,
        'product' : 8,
        'date': 17,
        'time': 18,
        'currency': 6         
    };
    
    # read raw data from file.
    file = open(csv_file, 'r');
    lines = file.readlines();
    file.close();
    
#    for i in range(1,len(lines)):
    for i in range(len(lines)):
        fields = lines[i].split(',');
        
        # deal with possible header
        try_field = fields[map['product']].strip().strip('"');
        if(try_field.upper() == 'Product'.upper()):            
            continue;
        
        if(fields[map['product_type']].strip().strip('"').lower() == 'spread'):
            continue;
        
        record = TradeRecord();
        
        record.account = fields[map['account']].strip().strip('"');
        if(len(record.account) > 6):
            record.account = record.account[0:6];
            
        product = fields[map['product']].strip().strip('"');
        product = get_standard_product_name(product);
        record.product = product;
        
        exchange = fields[map['exchange']].strip().strip('"');
        record.exchange = get_standard_exchange_name(exchange);
        
        
        record.bought_sold = fields[map['bought_sold']].strip().strip('"');
        record.price = float(fields[map['price']].strip());
        record.quantity = int(fields[map['quantity']])
        record.currency = fields[map['currency']].strip().strip('"');
        
        
        # deal with date and time
        # beause it is in GMT time, so timezone is needed.
        
#        # save old TZ
#        old_tz = None;
#        if('TZ' in os.environ):
#            old_tz = os.environ['TZ'];
#         
#        if(record.exchange.startswith('SGX')): 
#            os.environ['TZ'] = 'Asia/Singapore'
#        else:  
#            os.environ['TZ'] = 'UTC'
#        time.tzset();
#        
#        d = fields[map['date']].strip().strip('"');
#        t = fields[map['time']].strip().strip('"');
#        dt = d + ',' + t;
#        record.datetime = int(time.mktime(time.strptime(dt, '%m/%d/%Y,%I:%M:%S %p')));
#        
#        # restore TZ
#        if(old_tz is not None):
#            os.environ['TZ'] = old_tz;
#        else:
#            del os.environ['TZ']
#        time.tzset();
        
        # get the datetime
        d = fields[map['date']].strip().strip('"');
        t = fields[map['time']].strip().strip('"');
        dt = d + ',' + t;
        dt_obj = datetime.datetime.strptime(dt, '%m/%d/%Y,%I:%M:%S %p');
        
        # covert to the local time.
        tz = __exchange_open_time__[record.exchange]['TZ'];
        src_tz = 'UTC';
        if(record.exchange == 'SGX'):
            src_tz = 'Asia/Singapore'
            
        dt_obj = cu.convert_time(dt_obj, tz, src_tz);
        record.datetime = dt_obj;
        records.append(record);
        
    return records

def get_asap_trade_records(csv_file):
    records = [];
    map = {
        'account': 0,
        'bought_sold': 5,
        'quantity': 6,
        'exchange':1,
        'price' : 7,
        'product' : 2,
        'datetime': 3         
    };
    
    # read raw data from file.
    file = open(csv_file, 'r');
    lines = file.readlines();
    file.close();
    
#    for i in range(1,len(lines)):
    for i in range(len(lines)):
        fields = lines[i].split(',');
        
        # deal with possible header
        try_field = fields[map['product']].strip().strip('"');
        if(try_field.upper() == 'Instrument'.upper()):            
            continue;
        
        record = TradeRecord();
#        record.account = fields[map['account']].strip().strip('"');
#        record.product = fields[map['product']].strip().strip('"');
        
        
        record.account = fields[map['account']].strip().strip('"');
        if(len(record.account) > 6):
            record.account = record.account[0:6];
            
        product = fields[map['product']].strip().strip('"');
        product = get_standard_product_name(product);
        record.product = product;
        
        record.exchange = fields[map['exchange']].strip().strip('"');
        
        text = fields[map['bought_sold']].strip().strip('"');
        if(text.upper() == "SELL"):
            record.bought_sold = 'S';
        else:
            record.bought_sold = 'B';
        record.price = float(fields[map['price']].strip());
        record.quantity = int(fields[map['quantity']])
        
        
        #deal with timestamp
        dt = fields[map['datetime']].strip().strip('"');
        ts = re.findall('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', dt);
        
        record.datetime = datetime.datetime.strptime(ts[0], '%Y-%m-%d %H:%M:%S');
        
        if(record.exchange == 'SFE'):
            record.currency = 'AUD';
        
        records.append(record);
        
    return records            
        
def get_mfg_trade_records(xls_file, sheet_name='TradeActivity'):
    
    fields = ['Account', 'Contract', 'BoughtSold', 'Lots', 'Price', 'Exchange', 'curr', 'ClearComm', 'fees', 'GST', 'RunDate'];
    workBook = xlrd.open_workbook(xls_file);
    spreadsheet = workBook.sheet_by_name(sheet_name);
    
    # build field index
    index_map = {};
    for field in fields:
        for col in range(spreadsheet.ncols):
            if(field == spreadsheet.cell_value(0, col)):
                index_map[field] = col;
                break;
     
    # get records from xls file
    records = [];
    row = 1;
    while(row < spreadsheet.nrows):
        trade = TradeRecord()
        trade.account = str(spreadsheet.cell_value(row, index_map['Account']));
        trade.product = str(spreadsheet.cell_value(row, index_map['Contract']));
        trade.bought_sold = spreadsheet.cell_value(row, index_map['BoughtSold']);
        trade.quantity = int(spreadsheet.cell_value(row, index_map['Lots']));
        trade.price = spreadsheet.cell_value(row, index_map['Price']);
        trade.exchange = str(spreadsheet.cell_value(row, index_map['Exchange']));
        trade.currency = str(spreadsheet.cell_value(row, index_map['curr']));
        
        clearComm = spreadsheet.cell_value(row, index_map['ClearComm']);
        fees = spreadsheet.cell_value(row, index_map['fees']);
        
        trade.gst = round(abs(spreadsheet.cell_value(row, index_map['GST'])), 2);
        trade.commission = round(abs(clearComm) + abs(fees), 2);
        trade.mfgdate = str(spreadsheet.cell_value(row, index_map['RunDate']));
        
        
        records.append(trade);
        row = row + 1;
    return records;

def sort_trade_records(records):
    book = {}
    for record in records:
        __addtoindexbook__(book, record);
    return book;

def __addtoindexbook__(book, record):
    if record.account in book:
        if(record.product in book[record.account]):
            book[record.account][record.product].append(record);
        else:
            book[record.account][record.product] = [];
            book[record.account][record.product].append(record);
    else:
        book[record.account] = {}
        book[record.account][record.product] = [];
        book[record.account][record.product].append(record);
    
def match_trade_records(recordsA, recordsB):
    match_grp = [];
    mismatch_A = [];
    
    for record in recordsA:
        if(record in recordsB):
            match_grp.append(record);
            recordsB.remove(record);
        else:
            mismatch_A.append(record)
    
    return match_grp, mismatch_A, recordsB
        
def match_indexed_trade_records(bookA, bookB):
    match_book = {}
    mismatch_A = {}
    mismatch_B = {}
    
    for account in bookA:
        for product in bookA[account]:
            for record in bookA[account][product]:
                if(record.account in bookB and record.product in bookB[record.account]):
                    if(record in bookB[record.account][record.product]):
                        __addtoindexbook__(match_book, record);
                        bookB[record.account][record.product].remove(record)
                    else:
                        __addtoindexbook__(mismatch_A, record);
                else:
                    __addtoindexbook__(mismatch_A, record);
    
    for account in bookB:
        for product in bookB[account]:
            for record in bookB[account][product]:
                __addtoindexbook__(mismatch_B, record); 
                                                  
    return match_book, mismatch_A, mismatch_B;


def __fix_price__(record):
    name = get_standard_product_name(record.product);
    if(name == 'TN1'):
        price = record.price;
        i_price = int(price);
        f_price = price - i_price;
        f_price = f_price / 32;
        r_price = i_price + f_price;
        return round(r_price, 8);
    return record.price

def make_account_product_summary(book, MFG=False):
    sum_list = [];
    for account in book:
        for product in book[account]:
            aps = AccountProductSummary();
            aps.account = account;
            aps.product = product;
            b_qty = 0;
            s_qty = 0;
            
            sell_sum = 0;
            buy_sum = 0;
            commission = 0;
            gst = 0;
            
            name = get_standard_product_name(product);
            
            if(name in __product_tick_multiplier__):
                tick = __product_tick_multiplier__[name]['tick'];
                multiplier = __product_tick_multiplier__[name]['multiplier'];
                commission_rate = __product_tick_multiplier__[name]['commission'];
            else:
                tick = 0;
                multiplier = 0;
                commission = 0;
            
            
            for record in book[account][product]:
                if(record.bought_sold == 'S'):
                    s_qty = s_qty + record.quantity;
                    fixed_price = __fix_price__(record);
                    
                    if(record.product in ['ABBN', 'AXT', 'AYT']):
                        sell_sum += record.quantity * __cal__.getContractValue(record.product, record.price);
                    else:                                                                                
                        sell_sum += fixed_price * record.quantity * multiplier * tick;
                    
                     
                else:
                    b_qty = b_qty + record.quantity;
                    fixed_price = __fix_price__(record);
                    if(record.product in ['ABBN', 'AXT', 'AYT']):
                        buy_sum += record.quantity * __cal__.getContractValue(record.product, record.price);
                    else:
                        buy_sum += fixed_price * record.quantity * multiplier * tick;
                    
                aps.exchange = record.exchange;
                
                if(aps.product == "SNK"):
                    aps.currency = "JPY";
                    aps.fee_currency = "USD";
                else:
                    aps.currency = record.currency;
                    aps.fee_currency = record.currency;
                
                if(MFG is True):
                    commission += record.commission;
                    gst += record.gst;  
            
                        
            aps.buy_qty = b_qty;
            aps.sell_qty = s_qty;
            
            if(MFG is not True):
                commission = commission_rate * (b_qty + s_qty);
#                print commission;
                gst = 0.1 * commission;
            
            aps.profit = round(sell_sum - buy_sum, 3);
            aps.commission = round(commission, 3);
            aps.gst = round(gst, 3);
            
            sum_list.append(aps);
    return sum_list;
                
                


def is_same_account_product(dataA, dataB):
    # first compare account, the first 6 letter.
    accountA = dataA.account.upper()[0:6];
    accountB = dataB.account.upper()[0:6];
    if(accountA != accountB):
        return False;
    
    if(dataA.product == dataB.product):
            return True
        
    for name in __product_alias__:
        matchA = False;
        for pattern in name:
            if(re.match(pattern, dataA.product)):
                matchA = True;
                break;
        if(matchA is True):
            for pattern in name:
                if(re.match(pattern, dataB.product)):
                    return True;        
    
    return False;
    
    
    
def merge_account_product_summary(records):
    new_list = [];
    
    if(len(records) == 0):
        return new_list;
    
    record = records.pop();
    new_list.append(record);
    
    while(len(records) != 0):
        record = records.pop();
        merged = False;
        for item in new_list:
            if(is_same_account_product(record, item)):
                item.buy_qty = item.buy_qty + record.buy_qty;
                item.sell_qty = item.sell_qty + record.sell_qty;
                
                item.profit = round(item.profit + record.profit, 3);
                item.commission = round(item.commission + record.commission, 3);
                item.gst = round(item.gst + record.gst, 3);
                
                
                merged = True;
                break;
        if(merged is not True):
            new_list.append(record);
    
    return new_list;
    
def merge_with_open_positions(summary, open_position_records):
    for open_record in open_position_records:
        for record in summary:
            if(is_same_account_product(open_record, record)):
                record.open_qty = open_record.quantity;
                record.open_price = open_record.price;
                
                name = get_standard_product_name(record.product);
            
                if(name in __product_tick_multiplier__):
                    tick = __product_tick_multiplier__[name]['tick'];
                    multiplier = __product_tick_multiplier__[name]['multiplier'];
                else:
                    tick = 0;
                    multiplier = 0;
                
                if(record.product in ['ABBN','AXT','AYT']):
                    record.profit += open_record.quantity * __cal__.getContractValue(record.product, record.open_price);
                else:
                    record.profit += open_record.price * open_record.quantity * tick * multiplier;
                
                record.profit = round(record.profit, 3);
                break;
    return summary;
    
    
def merge_with_start_open_positions(summary, open_position_records):
    for open_record in open_position_records:
        for record in summary:
            if(is_same_account_product(open_record, record)):
                record.open_qty = open_record.quantity;
                record.open_price = open_record.price;
                
                name = get_standard_product_name(record.product);
            
                if(name in __product_tick_multiplier__):
                    tick = __product_tick_multiplier__[name]['tick'];
                    multiplier = __product_tick_multiplier__[name]['multiplier'];
                else:
                    tick = 0;
                    multiplier = 0;
                
#                record.profit -= open_record.price * open_record.quantity * tick * multiplier;
                
                if(record.product in ['ABBN','AXT','AYT']):
                    record.profit -= open_record.quantity * __cal__.getContractValue(record.product, record.open_price);
                else:
                    record.profit -= open_record.price * open_record.quantity * tick * multiplier;

                record.profit = round(record.profit, 3);
                break;            
    return summary;

def match_account_product_summary(listA, listB):
    match_list = [];
    mismatch_a = [];
    for item_a in listA:
        match_b = None;
        for item_b in listB:
            if(is_same_account_product(item_a, item_b)):
                if(item_a.buy_qty == item_b.buy_qty and item_a.sell_qty == item_b.sell_qty):
                    match_list.append(item_a);
                    match_b = item_b;
                    break;
        if(match_b is not None):
            listB.remove(match_b);
        else:
            mismatch_a.append(item_a);
            
    return match_list, mismatch_a, listB;
            
        


def __printtraderecords__(records, enable_header=True):
    lines = []
    if(enable_header is True):
        header = '%-10s%-10s%-10s%-10s%-10s' % ('account', 'product', 'type', 'price', 'quantity')
        lines.append(header);
    
    for record in records:
        line = '%-10s%-10s%-10s%-10s%-10s' % (record.account, record.product, record.bought_sold, record.price, record.quantity);
        lines.append(line);   
    return lines;



def print_acc_prod_summary(records, enable_header=True):
    lines = []
    if(enable_header is True):
        header = '%-10s%-10s%-10s%-10s%-10s%-10s' % ('exchange', 'account', 'product', 'buy_qty', 'sell_qty', 'difference')
        lines.append(header);
    
    for record in records:
        line = '%-10s%-10s%-10s%-10d%-10d%-10d' % (record.exchange, record.account, record.product, record.buy_qty, record.sell_qty, record.buy_qty - record.sell_qty);
        lines.append(line);   
    return lines;

                            
def generate_recon_report(template, match_list, mismatch_A, mismatch_B, source_list):
    file = open(template, 'r');
    lines = file.readlines();
    file.close();
    
    output = [];
    for line in lines:
        if(line.find('$MATCH_LIST$') != -1):
            output.extend(print_acc_prod_summary(match_list));
        elif(line.find('$MISMATCH_LIST_A$') != -1):
            output.extend(print_acc_prod_summary(mismatch_A));
        elif(line.find('$MISMATCH_LIST_B$') != -1):
            output.extend(print_acc_prod_summary(mismatch_B));
        elif(line.find('$MISMATCH_#_A$') != -1):
            line = line.replace('$MISMATCH_#_A$', '%d' % len(mismatch_A));
            output.append(line.strip());
        elif(line.find('$MISMATCH_#_B$') != -1):
            line = line.replace('$MISMATCH_#_B$', '%d' % len(mismatch_B));
            output.append(line.strip());
        elif(line.find('$MATCH_#$') != -1):
            line = line.replace('$MATCH_#$', '%d' % len(match_list));
            output.append(line.strip());
        elif(line.find('$SOURCE_LIST$') != -1):
            line = line.replace('$SOURCE_LIST$', '\n'.join(source_list));
            output.append(line.strip());
        else:
            output.append(line.strip());
            
    return output;


def get_open_positions(xls_file, sheet_name='AverageOP'):
    
    fields = ['Account', 'Contract', 'Volume', 'SettPrice'];
    workBook = xlrd.open_workbook(xls_file);
    spreadsheet = workBook.sheet_by_name(sheet_name);
    
    # build field index
    index_map = {};
    for field in fields:
        for col in range(spreadsheet.ncols):
            if(field == spreadsheet.cell_value(0, col)):
                index_map[field] = col;
                break;
     
    # get records from xls file
    records = [];
    row = 1;
    while(row < spreadsheet.nrows):
        trade = OpenPosition()
        trade.account = str(spreadsheet.cell_value(row, index_map['Account']));
        trade.product = str(spreadsheet.cell_value(row, index_map['Contract']));
        trade.quantity = int(spreadsheet.cell_value(row, index_map['Volume']));
        trade.price = spreadsheet.cell_value(row, index_map['SettPrice']);
        
        records.append(trade);
        row = row + 1;
    return records;
    
def get_PL_per_currency(summaries):
    book = {};
        
    for sum in summaries:
        curr = sum.currency;
        if(curr not in book):
            book[curr] = {};
            if(sum.currency != sum.fee_currency):
                book[curr][sum.account] = round(sum.profit);
            else:
                book[curr][sum.account] = round(sum.profit - sum.commission - sum.gst,3);
        else:
            if(sum.account not in book[curr]):
                
                if(sum.currency != sum.fee_currency):
                    book[curr][sum.account] = round(sum.profit);
                else:
                    book[curr][sum.account] = round(sum.profit - sum.commission - sum.gst,3);
                
            else:
                if(sum.currency != sum.fee_currency):
                    book[curr][sum.account] += sum.profit
                else:
                    book[curr][sum.account] += sum.profit - sum.commission - sum.gst;
                
                book[curr][sum.account] = round(book[curr][sum.account], 3);  
    return book;

def get_fee_per_currency(summaries):
    book = {};
        
    for sum in summaries:
        curr = sum.fee_currency;
        if(curr not in book):
            book[curr] = {};
            book[curr][sum.account] = round(sum.commission + sum.gst,3);
        else:
            if(sum.account not in book[curr]):
                book[curr][sum.account] = round(sum.commission + sum.gst,3);
            else:
                book[curr][sum.account] += sum.commission + sum.gst;
                book[curr][sum.account] = round(book[curr][sum.account], 3);  
    return book;
    
