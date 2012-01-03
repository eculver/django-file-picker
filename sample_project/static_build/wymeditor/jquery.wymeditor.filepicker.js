/*
 * WYMeditor plugin for django-file-picker
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

WYMeditor.editor.prototype.filepicker = function(options) {
    options = jQuery.extend({'rootURL': '/file-picker/'}, options);

    var wym = this,
        $element = jQuery(this._element);
        $box = jQuery(this._box);

    function installWYMEditorFilePicker(el, pickerNames, urls) {
        var pickers = {},
            buttonList = $box.find('div.wym_area_top ul'),
            names,
            overlay,
            fileButton,
            imageButton,
            audioButton,
            videoButton,
            youtubeButton,
            conf;

        $.each(pickerNames, function(type, name) {
            pickers[type] = urls[name];
        });

        playerOpts = {
            enableAutosize: true,
            pluginPath: '/static/mediaelement/',
            flashName: 'flashmediaelement.swf',
            silverlightName: 'silverlightmediaelement.xap',
            features: [
                'playpause',
                'progress',
                'current',
                'duration',
                'tracks',
                'volume',
                'fullscreen'
            ],
            audioWidth: '335',
            audioHeight: '30',
            videoWidth: '335',
            videoHeight: '250'
        };

        overlay = $('<div>').addClass('file-picker-overlay').overlay().filePicker({
            onImageClick: function(e, insert) {
                var wym = this.getRoot().parent().data('wym');
                wym.insert(insert);
                wym.update();
            },
            onAudioClick: function(e, insert) {
                var wym = this.getRoot().parent().data('wym');
                wym.insert(insert);
                playerOpts.success = function (player, node) { player.pause(); };
                $('audio,video').mediaelementplayer(playerOpts);
            },
            onVideoClick: function(e, insert) {
                var wym = this.getRoot().parent().data('wym');
                wym.insert(insert);
                playerOpts.success = function (player, node) { player.pause(); };
                $('audio,video').mediaelementplayer(playerOpts);
            }

        }).insertBefore($(el));

        if (pickers.file) {
            fileButton = $('<a>').text('Add File').attr({
                'title': 'File',
                'name': 'File',
                'href': '#'
            }).click(function(e) {
                e.preventDefault();
                $(overlay).data('wym', wym);
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.file;
                $(overlay).data('overlay').load();
            });

            buttonList.append($('<li>').addClass('wym_tools_file_add').append(fileButton));
        }

        if (pickers.image) {
            imageButton = $box.find('li.wym_tools_image a');
            imageButton.unbind();
            imageButton.click(function(e) {
                e.preventDefault();
                $(overlay).data('wym', wym);
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.image;
                $(overlay).data('overlay').load();
            });
        }

        if (pickers.audio) {
            audioButton = $('<a>').text('Add Audio').attr({
                'title': 'Audio',
                'name': 'Audio',
                'href': '#'
            }).click(function(e) {
                e.preventDefault();
                $(overlay).data('wym', wym);
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.audio;
                $(overlay).data('overlay').load();
            });

            buttonList.append($('<li>').addClass('wym_tools_audio_add').append(audioButton));
        }

        if (pickers.video) {
            videoButton = $('<a>').text('Add Video').attr({
                'title': 'Video',
                'name': 'Video',
                'href': '#'
            }).click(function(e) {
                e.preventDefault();
                $(overlay).data('wym', wym);
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.video;
                $(overlay).data('overlay').load();
            });

            buttonList.append($('<li>').addClass('wym_tools_video_add').append(videoButton));
        }

        if (pickers.youtube) {
            youtubeButton = $('<a>').text('Add YouTube Video').attr({
                'title': 'YouTube Video',
                'name': 'YouTube Video',
                'href': '#'
            }).click(function(e) {
                e.preventDefault();
                $(overlay).data('wym', wym);
                conf = $(overlay).data('filePicker').getConf();
                conf.url = pickers.youtube;
                $(overlay).data('overlay').load();
            });

            buttonList.append($('<li>').addClass('wym_tools_youtube_add').append(youtubeButton));
        }
    }

    // extract file picker names from element and get URLs via JSON
    pickerNames = getFilePickerTypes($element);

    if (pickerNames) {
        names = [];
        $.each(pickerNames, function(key, val) { names.push(val); });
        $.getJSON(options['rootURL'], {'pickers': names}, function(response) {
            installWYMEditorFilePicker($element, pickerNames, response.pickers);
        });
    }
};

$(document).ready(function() {
    $('textarea.wymeditor').each(function(idx, el) {
        $(el).wymeditor({
            updateSelector: 'input:submit',
            basePath: '/static/wymeditor/',
            skinPath: '/static/wymeditor/skins/twopanels/',
            skin: 'twopanels',
            stylesheet: '/static/wymeditor/skins/custom/wymeditor-custom.css',
            updateEvent: 'click',
            postInit: function(wym) {
                wym.filepicker();
            }
        });
    });
});
