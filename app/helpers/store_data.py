
class StoreBatchData(object):
    def __init__(self, data):
        self.raw_batch_data = data

    def append_to_history_cache(self):
        try:
            with open("scan_report_history_cache.log", "a") as cache_log:
                cache_log.write("")
                for d in self.raw_batch_data:
                    cache_log.write(f"Endpoint: {d['endpoint']}\n")
                    cache_log.write(f"Response Status: {d['response_status']}\n")
                    cache_log.write(f"Scan date: {d['scan_date']}\n")
                    cache_log.write("\n---\n")
                    cache_log.write("")
        except Exception as e:
            print(f"Error type: {type(e).__name__} - {e}")

    def get_history_cache(self):
        try:
            with open("scan_report_history_cache.log", "r") as cache_log:
                for line in self.raw_batch_data:
                    print(line)
        except Exception as e:
            print(f"Error type: {type(e).__name__} - {e}")

    def write_to_current_cache(self):
        try:
            with open("scan_report_current_cache.log", "w") as cache_log:
                for d in self.raw_batch_data:
                    cache_log.write(f"Endpoint: {d['endpoint']}\n")
                    cache_log.write(f"Response Status: {d['response_status']}\n")
                    cache_log.write(f"Scan date: {d['scan_date']}\n")
                    cache_log.write("\n---\n\n")
        except Exception as e:
            print(f"Error type: {type(e).__name__} - {e}")
    
    def get_current_cache(self):
        try:
            with open("scan_report_current_cache.log", "r") as cache_log:
                for line in cache_log:
                    print(line)
        except Exception as e:
            print(f"Error type: {type(e).__name__} - {e}")