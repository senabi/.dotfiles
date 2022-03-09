from Xlib import display
import sys


class Outputs:
    def __init__(self):
        self.d = display.Display()
        if not self.d.has_extension('RANDR'):
            sys.stderr.write(
                f'{sys.argv[0]}: server does not have the RANDR extension\n')
            ext = self.d.query_extension('RANDR')
            print(ext)
            sys.stderr.write("\n".join(self.d.list_extensions()))
            if ext is None:
                sys.exit(1)

        # current screen
        self.screen = self.d.screen()
        resources = self.screen.root.xrandr_get_screen_resources()._data

        self.outputs_list = []
        for output in resources['outputs']:
            output_info = self.d.xrandr_get_output_info(
                output, resources['config_timestamp'])._data
            if not output_info['crtc']:
                continue
            # self.pp.pprint(output_info)
            crtc = self.d.xrandr_get_crtc_info(
                output_info['crtc'], resources['config_timestamp'])._data
            self.outputs_list.append(
                {'name': output_info['name'],
                    'height': crtc['height'], 'width': crtc['width']})

    def get_list(self):
        return self.outputs_list
