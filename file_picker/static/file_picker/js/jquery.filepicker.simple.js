/*
 * Simple jQuery plugin for use with django-file-picker
 * Author: Caktus Consulting Group, LLC (http://www.caktusgroup.com/)
 * Source: https://github.com/caktus/django-file-picker
 *
 * Copyright (C) 2011 by Caktus Consulting Group, LLC
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
 
jQuery(document).ready(function($) {

    var FILE_PICKER_ROOT = '/file-picker/';

    function installFilePicker(el, pickerNames, urls) {
        var pickers = {}, overlay, parent, anchor, conf;

        $.each(pickerNames, function(type, name) {
            pickers[type] = urls[name];
        });
        overlay = $('<div>').addClass('file-picker-overlay').overlay().filePicker({
            onImageClick: function(e, insert) {
                insertAtCaret(el.id, insert);
            },
            onAudioClick: function(e, insert) {
                insertAtCaret(el.id, insert);
            },
            onVideoClick: function(e, insert) {
                insertAtCaret(el.id, insert);
            }
        }).insertBefore($(el));

        parent = $(el).parent();

        if (pickers.file) {
            anchor = $('<a>').text('Insert File').attr({
                'name': 'filepicker-file',
                'title': 'Insert File',
                'href': '#'
            }).css('display', 'block').click(function(e) {
                e.preventDefault();
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.file;
                $(overlay).data('overlay').load();
            }).prependTo(parent);
        }

        if (pickers.image) {
            anchor = $('<a>').text('Insert Image').attr({
                'name': 'filepicker-image',
                'title': 'Insert Image',
                'href': '#'
            }).css('display', 'block').click(function(e) {
                e.preventDefault();
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.image;
                $(overlay).data('overlay').load();
            }).prependTo(parent);
        }

        if (pickers.audio) {
            anchor = $('<a>').text('Insert Audio').attr({
                'name': 'filepicker-audio',
                'title': 'Insert Audio',
                'href': '#'
            }).css('display', 'block').click(function(e) {
                e.preventDefault();
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.audio;
                $(overlay).data('overlay').load();
            }).prependTo(parent);
        }

        if (pickers.video) {
            anchor = $('<a>').text('Insert Video').attr({
                'name': 'filepicker-video',
                'title': 'Insert Video',
                'href': '#'
            }).css('display', 'block').click(function(e) {
                e.preventDefault();
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.video;
                $(overlay).data('overlay').load();
            }).prependTo(parent);
        }
    }

    $('textarea.simple-filepicker').each(function(idx, el) {
        var pickerNames = getFilePickerTypes(el),
            names = [];

        if (pickerNames) {
            $.each(pickerNames, function(key, val) { names.push(val); });
            $.getJSON(FILE_PICKER_ROOT, {'pickers': names}, function(response) {
                installFilePicker(el, pickerNames, response.pickers);
            });
        }
    });
});
