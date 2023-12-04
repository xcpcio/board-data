#! /usr/bin/env python3

import os

from xcpcio_board_spider import utils

dist_path = "../../data/index"
dist = os.path.join(dist_path, "contest_list.json")
pathname = "../../data"
contest_list = {}


def dfs(contest_list, pathname, board_link):
    if pathname.endswith('-assets'):
        return

    config_path = os.path.join(pathname, "config.json")
    if os.path.isfile(config_path):
        config = utils.json_input(config_path)

        contest_list['config'] = {}
        contest_list['config']['contest_name'] = config['contest_name']
        contest_list['config']['start_time'] = config['start_time']
        contest_list['config']['end_time'] = config['end_time']
        contest_list['config']['frozen_time'] = config['frozen_time']

        if 'link' in config.keys():
            contest_list['config']['link'] = config['link']

        if 'logo' in config.keys():
            contest_list['config']['logo'] = config['logo']

        contest_list['board_link'] = board_link
    else:
        for _path in os.listdir(pathname):
            if not _path in ['index', '.gitignore', '.DS_Store']:
                contest_list[_path] = {}
                dfs(contest_list[_path], os.path.join(
                    pathname, _path), os.path.join(board_link, _path))


def main(contest_list, pathname):
    dfs(contest_list, pathname, '/')

    utils.ensure_makedirs(dist_path)
    utils.output(dist, contest_list)


if __name__ == '__main__':
    main(contest_list, pathname)
