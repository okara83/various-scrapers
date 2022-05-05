class InfiniteScroll:
    def __init__(self, previous_height, log):
        self.previous_height = previous_height
        self.log = log

    def __call__(self, driver, *args, **kwargs):

        new_height = driver.execute_script("return document.body.scrollHeight")
        self.log.debug(dict(ph=self.previous_height, nh=new_height))

        if new_height > self.previous_height:
            return new_height

        return False
