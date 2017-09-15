#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest
from os import path, mkdir, listdir
import shutil
from PIL import Image
from sys import path as sys_path
__dirname__ = path.dirname(path.realpath(__file__))
sys_path.append(path.realpath(path.join(__dirname__, '..')))
import manga
from helpers import remove_void as cropper


class Arguments:
    def setArgument(self, name, value):
        setattr(self, name, value)

    def setArguments(self, arguments):
        for name, value in arguments:
            self.setArgument(name, value)


class TestCase(unittest.TestCase):
    def setUp(self):
        self.current_id = ''
        self.root_path = __dirname__
        self.path = path.join(self.root_path, 'temp')
        self.arguments = Arguments()
        self.arguments.setArguments([  # default arguments
            # ('url', None),
            ('name', 'Manga'),
            ('destination', self.path),
            ('info', False),
            ('progress', False),
            ('skip_volumes', 0),
            ('user_agent', ''),
            ('no_name', False),
            ('allow_webp', False),
            ('reverse_downloading', False),
            ('rewrite_exists_archives', False),
            ('xt', 0),
            ('xr', 0),
            ('xb', 0),
            ('xl', 0),
            ('crop_blank', False),
            ('crop_blank_factor', 100),
            ('crop_blank_max_size', 30),
            ('max_volumes', 1),
        ])

    def _prepare_arguments(self):
        setattr(manga, 'info_mode', self.arguments.info)
        setattr(manga, 'show_progress', self.arguments.progress)
        setattr(manga, 'add_name', not self.arguments.no_name)
        setattr(manga, 'name', self.arguments.name)
        if len(self.arguments.user_agent):
            setattr(manga, 'user_agent', self.arguments.user_agent)

        setattr(manga, 'add_name', not self.arguments.no_name)
        setattr(manga, 'arguments', self.arguments)


    def _before_test(self):
        if path.isdir(self.path):
            shutil.rmtree(self.path)
        mkdir(self.path)

    def __test_url(self, url):
        self.arguments.setArgument('url', url)
        self._prepare_arguments()
        downloader = manga.MangaDownloader(url, self.arguments.name)
        self.assertTrue(downloader.status)

        downloader.process()

        count_files = len([name for name in listdir(self.path)])
        return count_files > 0

    def test_error_url(self):
        self.__test_url('http://failed.path.to/manga')

    def _urls_true(self, urls):
        self._before_test()
        for url in urls:
            self.assertTrue(self.__test_url(url))

    def _urls_false(self, urls):
        self._before_test()
        for url in urls:
            self.assertFalse(self.__test_url(url))

    def _prepare_cropper(self, need_copy=True, img_name='img1.jpg'):
        self._before_test()
        source_file = path.join(self.root_path, img_name)
        tested_file = path.join(self.path, img_name)

        if need_copy:
            shutil.copyfile(source_file, tested_file)

        return source_file, tested_file

    def test_cropper1(self):
        source_file, tested_file = self._prepare_cropper()

        cropper.crop(tested_file, {'left': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        left_sizes = source_sizes = source_image.sizes()
        tested_sizes = tested_image.sizes()
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 0)

        shutil.copyfile(source_file, tested_file)
        cropper.crop(tested_file, {'right': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.sizes()
        tested_sizes = tested_image.sizes()
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 0)
        self.assertTrue(tested_sizes[0] == left_sizes[0])

    def test_cropper2(self):
        source_file, tested_file = self._prepare_cropper()

        cropper.crop(tested_file, {'top': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        top_sizes = source_sizes = source_image.sizes()
        tested_sizes = tested_image.sizes()
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 0)

        shutil.copyfile(source_file, tested_file)
        cropper.crop(tested_file, {'bottom': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.sizes()
        tested_sizes = tested_image.sizes()
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 0)
        self.assertTrue(tested_sizes[0] == top_sizes[0])

    def test_cropper3(self):
        # source_file, tested_file = self._prepare_cropper(False)
        # cropper.process(source_file, tested_file)
        pass

    def test_cropper4(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img1.jpg')
        tested_file = path.join(self.path, 'img1.jpg')
        shutil.copyfile(source_file, tested_file)
        pass

    def test_cropper5(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img1.jpg')
        tested_file = path.join(self.path, 'img1.jpg')
        shutil.copyfile(source_file, tested_file)
        pass

    def test_balumanga_com(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'http://bulumanga.com/mangaView.html?id=1&cid=34701&page=1&source=mangareader',
                'http://bulumanga.com/introduce.html?id=34701&source=mangareader',
            ],
            'error': [
                'http://bulumanga.com/introduce.html?id=0'
            ],
        }
        self._urls_true(urls['success'])
        self._urls_false(urls['error'])

    def test_com_x_life(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'https://com-x.life/4156-teenage-mutant-ninja-turtles-universe.html',
                'https://com-x.life/3882-grendel.html',
            ],
            'error': [
                'https://com-x.life/0-none.html'
                'https://com-x.life/0-false.html'
            ],
        }

    def test_bato_to(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'https://bato.to/comic/_/comics/karakai-jouzu-no-takagi-san-r13108',
                'https://bato.to/comic/_/comics/mousou-telepathy-r19915',
            ],
            'error': [
                'https://bato.to/comic/omics/mousou-telepathy-r19915'
            ],
        }

if __name__ == '__main__':
    unittest.main()