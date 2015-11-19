'''
Created on 2011-4-1

@author: michael
'''
import tradeutils as trade

class Recon(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.mfgRecords = [];
        self.epochRecords = [];
        self.startPositions =[];
        self.endPositions = [];
        
    
    def reconcile(self):
        # deal with MFG data
        sortedList = trade.sort_trade_records(self.mfgRecords);
        mfgSum = trade.make_account_product_summary(sortedList, MFG=True);
        mfgSum = trade.merge_with_start_open_positions(mfgSum, self.startPositions);
        mfgSum = trade.merge_with_open_positions(mfgSum, self.endPositions);
        
        # deal with Epoch data
        sortedList = trade.sort_trade_records(self.epochRecords);
        epochSum = trade.make_account_product_summary(sortedList, MFG=False);
        epochSum = trade.merge_account_product_summary(epochSum);
        epochSum = trade.merge_with_start_open_positions(epochSum, self.startPositions);
        epochSum = trade.merge_with_open_positions(epochSum, self.endPositions);
        
        match_result = [];
        for item_mfg in mfgSum:
            match_epoch = None;
            for item_epoch in epochSum:
                if(trade.is_same_account_product(item_mfg, item_epoch)):
                    if(item_mfg.buy_qty == item_epoch.buy_qty and item_mfg.sell_qty == item_epoch.sell_qty):
                        #match
                        match = ('MATCH', item_mfg, item_epoch);
                    else:
                        match = ('MISMATCH', item_mfg, item_epoch);
                    match_result.append(match);
                    match_epoch = item_epoch;
                    break;
            if(match_epoch is not None):
                epochSum.remove(match_epoch);
            else:
                match = ('MISMATCH', item_mfg, None);
                match_result.append(match);
        # deal rest of epoch data
        for item_epoch in epochSum:
            match = ('MISMATCH', None, item_epoch);
            match_result.append(match);
            
        return match_result;
    
    
    def generate_csvreport(self,match_list):
        report = [];
        header = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % ('STATUS', 'exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
        header1 = ',%s,%s,%s,%s,%s,%s,%s,%s,%s' % ('exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
        header = header + header1;
        report.append(header);
        for entry in match_list:
            (flag, mfg_item, epoch_item) = entry;
            status = '%s,' % flag;
            if(mfg_item is not None):
                mfg = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (mfg_item.exchange, mfg_item.account, mfg_item.product, mfg_item.buy_qty, mfg_item.sell_qty, mfg_item.profit, mfg_item.commission, mfg_item.gst, mfg_item.profit - mfg_item.commission- mfg_item.gst);
            else:
                mfg = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (' ',' ',' ',' ',' ',' ',' ',' ',' ');
                
            if(epoch_item is not None):
                epoch = ',%s,%s,%s,%s,%s,%s,%s,%s,%s' % (epoch_item.exchange, epoch_item.account, epoch_item.product, epoch_item.buy_qty, epoch_item.sell_qty,epoch_item.profit, epoch_item.commission, epoch_item.gst, epoch_item.profit - epoch_item.commission - epoch_item.gst);
            else:
                epoch = ',%s,%s,%s,%s,%s,%s,%s,%s,%s' % (' ',' ',' ',' ',' ',' ',' ',' ',' ');
                
            line = status + mfg + epoch
            report.append(line);
        return report;