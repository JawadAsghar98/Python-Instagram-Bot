import codecs
import errno
import json
import os
import time

# from instagram_scraper.constants import *


class InstagramScraper(object):

    def __init__(self, **kwargs):
        self.last_scraped_filemtime = 0
        default_attr = {'username': '', 'usernames': [], 'filename': None, 'login_user': None, 'login_pass': None,
                        'followings_input': False, 'followings_output': 'profiles.txt', 'destination': './',
                        'logger': None, 'retain_username': False, 'interactive': False, 'quiet': False,
                        'maximum': 0, 'media_metadata': False, 'profile_metadata': False, 'latest': False,
                        'latest_stamps': False, 'cookiejar': None, 'filter_location': None,
                        'filter_locations': None, 'media_types': ['image', 'video', 'story-image', 'story-video'],
                        'tag': False, 'location': False, 'search_location': False, 'comments': False, 'verbose': 0,
                        'include_location': False, 'filter': None, 'proxies': {}, 'no_check_certificate': False,
                        'template': '{urlname}', 'log_destination': ''}

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

    def get_dst_dir(self, username):
        """Gets the destination directory and last scraped file time."""
        if self.destination == './':
            dst = './' + username
        else:
            if self.retain_username:
                dst = self.destination + '/' + username
            else:
                dst = self.destination

    def make_dir(self, dst):
        try:
            os.makedirs(dst)
        except OSError as err:
            if err.errno == errno.EEXIST and os.path.isdir(dst):
                # Directory already exists
                pass
            else:
                # Target dir exists as a file, or a different error
                raise

    def scrape_hashtag(self):
        self.__scrape_query(self.query_hashtag_gen)

    def query_hashtag_gen(self, hashtag):
        return self.__query_gen(QUERY_HASHTAG, QUERY_HASHTAG_VARS, 'hashtag', hashtag)

    def __query_gen(self, url, variables, entity_name, query, end_cursor=''):
        """Generator for hashtag and location."""
        nodes, end_cursor = self.__query(url, variables, entity_name, query, end_cursor)

        if nodes:
            try:
                while True:
                    for node in nodes:
                        yield node

                    if end_cursor:
                        nodes, end_cursor = self.__query(url, variables, entity_name, query, end_cursor)
                    else:
                        return
            except ValueError:
                self.logger.exception('Failed to query ' + query)

    def _get_nodes(self, container):
        return [self.augment_node(node['node']) for node in container['edges']]

    def __query_media(self, id, end_cursor=''):
        params = QUERY_MEDIA_VARS.format(id, end_cursor)
        self.update_ig_gis_header(params)

        resp = self.get_json(QUERY_MEDIA.format(params))

        if resp is not None:
            payload = json.loads(resp)['data']['user']

            if payload:
                container = payload['edge_owner_to_timeline_media']
                nodes = self._get_nodes(container)
                end_cursor = container['page_info']['end_cursor']
                return nodes, end_cursor

        return None, None

    def has_selected_media_types(self, item):
        filetypes = {'jpg': 0, 'mp4': 0}

        for url in item['urls']:
            ext = self.__get_file_ext(url)
            if ext not in filetypes:
                filetypes[ext] = 0
            filetypes[ext] += 1

        if ('image' in self.media_types and filetypes['jpg'] > 0) or \
                ('video' in self.media_types and filetypes['mp4'] > 0):
            return True

        return False

    def story_has_selected_media_types(self, item):
        # media_type 1 is image, 2 is video
        if item['__typename'] == 'GraphStoryImage' and 'story-image' in self.media_types:
            return True
        if item['__typename'] == 'GraphStoryVideo' and 'story-video' in self.media_types:
            return True

        return False

    def extract_tags(self, item):
        """Extracts the hashtags from the caption text."""
        caption_text = ''
        if 'caption' in item and item['caption']:
            if isinstance(item['caption'], dict):
                caption_text = item['caption']['text']
            else:
                caption_text = item['caption']

        elif 'edge_media_to_caption' in item and item['edge_media_to_caption'] and item['edge_media_to_caption'][
            'edges']:
            caption_text = item['edge_media_to_caption']['edges'][0]['node']['text']

    def download(self, item, save_dir='./'):
        """Downloads the media file."""
        for full_url, base_name in self.templatefilename(item):
            url = full_url.split('?')[0]  # try the static url first, stripping parameters

            file_path = os.path.join(save_dir, base_name)

            if not os.path.exists(os.path.dirname(file_path)):
                self.make_dir(os.path.dirname(file_path))

                part_file = file_path + '.part'
                downloaded = 0
                total_length = None
                with open(part_file, 'wb') as media_file:
                    try:
                        retry = 0
                        retry_delay = RETRY_DELAY
                        while (True):
                            if self.quit:
                                return
                        downloaded_before = downloaded
                    except:
                        time.sleep(3)

    def merge_json(self, data, dst='./'):
        if not os.path.exists(dst):
            self.save_json(data, dst)

        if data:
            merged = data
            with open(dst, 'rb') as f:
                file_data = json.load(codecs.getreader('utf-8')(f))
                key = list(merged.keys())[0]
                if key in file_data:
                    merged[key] = file_data[key]
            self.save_json(merged, dst)

    @staticmethod
    def save_json(data, dst='./'):
        """Saves the data to a json file."""
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))

        if data:
            output_list = {}
            if os.path.exists(dst):
                with open(dst, "rb") as f:
                    output_list.update(json.load(codecs.getreader('utf-8')(f)))

            with open(dst, 'wb') as f:
                output_list.update(data)
                json.dump(output_list, codecs.getwriter('utf-8')(f), indent=4, sort_keys=True, ensure_ascii=False)


def main():
    main()
