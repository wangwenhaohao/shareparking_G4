from SharedParkingPlace.kw_ui_script.collection import Collection
from SharedParkingPlace.tools.fileutil import FileUtil


class Start:
    def run(self):
        co = Collection
        kw_map = FileUtil.get_json('intepret')
        test_script_path = FileUtil.get_txt_line('script_conf')
        for script_path in test_script_path:
            scripts = FileUtil.get_txt_line(script_path)
            for step in scripts:
                temp = step.split(',')
                keyword = temp[0]
                params = tuple(temp[1:])
                if hasattr(co, kw_map[keyword]):
                    fun = getattr(co, kw_map[keyword])
                    fun(*params)


if __name__ == '__main__':
    Start().run()
