/*
 * jQuery plugin for django-file-picker
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
"use strict";

(function ($) {

    // don't use square bracket syntax (jQuery 1.4.x)
    // source: http://benalman.com/news/2009/12/jquery-14-param-demystified/
    $.ajaxSetup({ traditional: true });

    $.filePicker = {
        conf: {
            url: '',
            urls: ''
        }
    };

    // constructor
    function FilePicker(root, conf) {
        // current instance
        var self = this,
            tabs = null,
            panes = null,
            browsePane = null,
            uploadPane = null;

        root.data('overlay').onLoad(function () {
            this.getOverlay().data('filePicker').load();
            $('.file-picker-overlay').css('z-index', '1');
            $('img').css('z-index', '0');
        });

        root.data('overlay').onClose(function () {
            browsePane.empty();
            uploadPane.empty();
            $('.plupload').remove();
        });

        root.append($('<div>').addClass('file-picker'));
        root = root.find('.file-picker');

        // methods
        $.extend(self, {
            getConf: function () {
                return conf;
            },

            getRoot: function () {
                return root;
            },

            load: function () {
                tabs.tabs('div.panes > div.pane');
                $(tabs).data('tabs').onClick(function (e, index) {
                    self.tabClick(e, index);
                });

                $.get(conf.url, function (response) {
                    conf.urls = response.urls;
                    self.getFiles();
                });
            },

            tabClick: function (e, index) {
                $('.plupload').remove();
                if (index === 1) {
                    self.getForm();
                } else if (index === 0) {
                    self.getFiles();
                }
            },

            getForm: function (data) {
                var uploadForm, submit;

                if (!data) {
                    $.get(conf.urls.upload.file, {}, function (response) {
                        self.displayForm(response);
                        self.setupUpload();
                    });
                } else {
                    $.post(conf.urls.upload.file, data, function (response) {
                        if (response.errors) {
                            $.each(response.errors, function (idx) {
                                console.error(this);
                            });
                            return;
                        }

                        if (response.insert) {
                            $(self).trigger("onImageClick", [response.insert]);
                            self.getForm();
                        } else {
                            self.displayForm(response);
                            self.setupUpload();
                        }
                    });
                }
            },

            displayForm: function (data) {
                var pane, browse, runtime, form, table, submit, uploadForm;

                pane = root.find('.file-picker-upload');
                pane.empty();
                pane.append($('<h2>').text('Select file to upload'));

                browse = $('<input>').val('Select a file').attr({
                    'type': 'button',
                    'id': 'select-a-file'
                }).addClass('select-a-file');
                pane.append(browse);

                runtime = $('<div>').addClass('runtime');
                pane.append(runtime);
                pane.append($('<ul>').addClass('upload-list'));
                pane.append($('<h3>').text('File details'));

                form = $('<form>').attr({
                    'method': 'post',
                    'class': 'upload_form',
                    'action': ""
                });

                table = $('<table>').html(data.form);
                /*
                submit = $('<input>').attr({
                    'type': 'submit',
                    'value': 'Submit'
                }).click(function (e) {
                    e.preventDefault();
                    uploadForm = uploadPane.find('.upload_form');
                    data = {};
                    $(':input', uploadForm).each(function () {
                        data[this.name] = this.value;
                    });
                    self.getForm(data);
                });
                */
                form.append(table);
                form.append(submit);

                pane.append(form);
            },

            getFiles: function (data) {
                if (!data) {
                    data = {};
                }
                $.get(conf.urls.browse.files, data, function (response) {
                    self.displayFiles(response);
                });
            },

            setupUpload: function () {
                var ajaxUpload = new AjaxUpload('select-a-file', {
                    action: conf.urls.upload.file,
                    autoSubmit: true,
                    responseType: 'json',
                    onSubmit: function(file, extension) {
                        $('.runtime').html('Uploading ...');
                        $('.add_to_model').remove();
                    },
                    onComplete: function(file, response) {
                        var submit, uploadForm;

                        $('.runtime').html('Uploading ... Complete');

                        submit = $('<input>').attr({
                            'class': 'add_to_model',
                            'type': 'submit',
                            'value': 'Submit'
                        }).click(function (e) {
                            var data = {};

                            e.preventDefault();
                            uploadForm = uploadPane.find('.upload_form');
                            $(':input', uploadForm).each(function () {
                                data[this.name] = this.value;
                            });
                            data.file = response.name;
                            self.getForm(data);
                        });
                        uploadForm = uploadPane.find('.upload_form');
                        uploadForm.append(submit);
                    }
                });
            },

            displayFiles: function (data) {
                var files = data.result,
                    table, tr, form, div, footer, next, previous, trigger;

                browsePane.empty();
                browsePane.append($('<h2>').text('Select file to insert'));
                table = $('<table>').addClass('file-list');
                tr = $('<tr>');
                form = $('<form>').attr({
                    'action': "",
                    'method': 'get',
                    'class': 'file-picker-search'
                });
                form.append(
                    $('<input>').attr({
                        'type': 'text',
                        'class': 'search_val',
                        'name': 'search'
                    }).val(data.search));
                form.append(
                    $('<input>').attr({
                        'type': 'submit',
                        'value': 'Search'
                    }).addClass('search_val').click(function (e) {
                        e.preventDefault();
                        self.getFiles({
                            'search': browsePane.find('.search_val').val()
                        });
                    }));
                if (files.length > 0) {
                    tr = $('<tr>');
                    $.each(data.link_headers, function (idx, value) {
                        tr.append($('<th>').text(value));
                    });
                    $.each(data.extra_headers, function (idx, value) {
                        tr.append($('<th>').text(value));
                    });
                }
                table.append(tr);
                $.each(files, function (idx, file) {
                    var tr = $('<tr>'), a;
                    $.each(file.link_content, function (idx, value) {
                        a = $('<a>').click(function (e) {
                            $(self).trigger("on" + data.model + "Click", [file.insert[idx]]);
                        });
                        a.append(value);
                        tr.append($('<td>').append(a));
                    });
                    $.each(data.columns, function (idx, key) {
                        tr.append($('<td>').append(file.extra[key]));
                    });
                    table.append(tr);
                });
                div = $('<div>').attr({'class': 'scrollable'});
                browsePane.append(form);
                browsePane.append(div.append(table));
                footer = $('<div>').attr('class', 'footer');
                next = $('<a>').attr({
                    'title': 'Next',
                    'href': '#'
                }).text('Next');

                if (data.has_next) {
                    next.click(function (e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page + 1, 
                        'search': browsePane.find('.search_val').val()});
                    });
                } else {
                    next.css('color', '#bbb');
                }

                previous = $('<a>').attr({
                    'title': 'Next',
                    'href': '#'
                }).text('Previous ');

                if (data.has_previous) {
                    previous.click(function (e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page - 1, 
                        'search': browsePane.find('.search_val').val()});
                    });
                } else {
                    previous.css('color', '#bbb');
                }
                footer.append(previous);
                $.each(data.pages, function (index, value) { 
                    var list = $('<a>').attr({
                        'title': value,
                        'href': '#'
                    }).text(value + ' ');
                    if (data.page === value) {
                        list.css('color', '#bbb');
                    } else {
                        list.click(function (e) {
                            e.preventDefault();
                            self.getFiles({
                                'page': value, 
                                'search': browsePane.find('.search_val').val()
                            });
                        });
                    }
                    footer.append(list);
                });
                footer.append(next);
                browsePane.append(footer);
            }
        });

        // callbacks
        $.each(['onImageClick', 'onAudioClick', 'onVideoClick', 'onSlideshowClick'], function (i, name) {
            // configuration
            if ($.isFunction(conf[name])) { 
                $(self).bind(name, conf[name]); 
            }
            self[name] = function (fn) {
                $(self).bind(name, fn);
                return self;
            };
        });

        // setup tabs
        tabs = $('<ul>').addClass('css-tabs').addClass('file-picker-tabs');
        tabs.append($('<li>').append($('<a>').attr('href', '#').text('Browse')));
        tabs.append($('<li>').append($('<a>').attr('href', '#').text('Upload')));
        panes = $('<div>').addClass('panes');
        browsePane = $('<div>').addClass('file-picker-browse').addClass('pane');
        browsePane.append($('<h2>').text('Browse for a file'));
        panes.append(browsePane);
        uploadPane = $('<div>').addClass('file-picker-upload').attr({'id': 'file-picker-upload'}).addClass('pane');
        panes.append(uploadPane);
        root.append(tabs);
        root.append(panes);
    }


    // jQuery plugin implementation
    $.fn.filePicker = function (conf) {
        // already constructed --> return API
        var el = this.data("filePicker");

        if (el) {
            return el;
        }

        conf = $.extend({}, $.filePicker.conf, conf);

        this.each(function () {
            el = new FilePicker($(this), conf);
            $(this).data("filePicker", el);
        });

        return conf.api ? el: this;
    };
})(jQuery);


function getFilePickerTypes(el) {
    var pickerNames = {},
        type, name;

    $.each($(el).attr('class').split(' '), function(idx, className) {
        if (className.substr(0, 17) == 'file_picker_name_') {
            type = className.split('_')[3];
            name = className.split('_')[4];
            pickerNames[type] = name;
        }
    });
    return pickerNames;
}

function insertAtCaret(areaId, text) {
    var txtarea = document.getElementById(areaId),
        scrollPos = txtarea.scrollTop,
        strPos = 0,
        br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? "ff" : (document.selection ? "ie" : false ) ),
        range,
        front,
        back;

    if (br == "ie") { txtarea.focus();
        range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    } else if (br == "ff") strPos = txtarea.selectionStart;

    front = (txtarea.value).substring(0,strPos);
    back = (txtarea.value).substring(strPos,txtarea.value.length);
    txtarea.value=front+text+back;
    strPos = strPos + text.length;

    if (br == "ie") {
        txtarea.focus();
        range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    } else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }

    txtarea.scrollTop = scrollPos;
}
