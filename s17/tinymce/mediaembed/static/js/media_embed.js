tinyMCEPopup.requireLangPack();

var MediaEmbedDialog = {
    init : function() {
        var f = $('#media-form');

        // Get the selected contents as text and place it in the input
        //f.someval.value = tinyMCEPopup.editor.selection.getContent({format : 'text'});
        //f.somearg.value = tinyMCEPopup.getWindowArg('some_custom_arg');

        //onload we should see a list of elements
        this.get_folder_listing();
        //make some basic event initialization

        //search
        var search_button = $('input[name="search-button"]', f);
        search_button.click(function(e){
            var search_text = $('input[name="search"]', f);
            var media_type = $('input[name="media_type"]:checked', f);

            MediaEmbedDialog.get_folder_listing(
                search_text.val(), 
                tinyMCEPopup.editor.settings.navigation_root_url, 
                media_type.val(),
                0
            );
            e.preventDefault();
        });
    },

    get_folder_listing : function(text, path, media_type, folders){
        if (!path){
            path = tinyMCEPopup.editor.settings.navigation_root_url;
        }
        $.ajax({
            url: path + '/@@media_search',
            data:{
                'search_for':text, 
                'media_type':media_type,
                'folders': folders
            },
            dataType:'json',
            success:function(data){
                var container = $('<div/>');
                if (data[0] !== undefined){
                    $.each(data, function(elem){
                        var element = $('<div class="item"/>');
                        var link = $('<a/>');
                        var radio = $('<input type="radio" class="noborder" name="internallink" />');
                        link.attr('title', this.title);
                        link.attr('href', this.url);
                        link.html(this.title);
                        link.data('itype', this.itype);

                        if (!this.is_folderish){
                            element.append(radio);
                            link.addClass('media-link');
                        } else {
                            link.addClass('folderish');
                        }
                        element.append(link);
                        container.append(element);
                    });
                } else {
                    container.html('<p>No Results</p>');
                }
                $('.panel .folder-listing').html(container);

                //check the input if we click in a media link
                $('.panel .folder-listing .media-link').click(function(e){
                    $(this).siblings('input').click();
                    e.preventDefault();
                });
                
                //lets create the preview
                $('.panel .folder-listing .media-link').siblings('input').click(function(e){
                    var metadata = $(this).siblings('a');
                    var preview = $('<div/>');
                    var link = $('<a class="'+ metadata.data('itype') +'" href="'+metadata.attr('href')+'"></a>');
                    var dimmensions = $('<div>Width: <input name="media_width" type="text" size="10"/> Height: <input name="media_height" type="text" size="10"/></div>');
                    var h = '300';
                    var w = '425';
                    preview.append(link);
                    preview.append(dimmensions);

                    $('.preview').html(preview);
                    if ($('.video')[0] !== undefined){
                        link.attr('style',"display:block;width:425px;height:300px;");
                        flowplayer("a.video", "++resource++s17.media.views/flowplayer/flowplayer-3.2.7.swf");
                        $(dimmensions).find('input[name="media_width"]').val(w);
                        $(dimmensions).find('input[name="media_height"]').val(h);
                    }

                    if ($('.audio')[0] !== undefined){
                        link.attr('href', link.attr('href') + '?e=.mp3');
                        link.attr('style',"display:block;width:425px;height:30px;");
                        $(dimmensions).find('input[name="media_width"]').val(w);
                        $(dimmensions).find('input[name="media_height"]').val(30);
                        flowplayer("a.audio", "++resource++s17.media.views/flowplayer/flowplayer-3.2.7.swf", {
                            plugins: {
                                controls: {
                                    fullscreen: false,
                                    height: 30,
                                    autoHide: false
                                }
                            },
                            clip: {
                                autoPlay: false,

                                // optional: when playback starts close the first audio playback
                                onBeforeBegin: function() {
                                    $f("player").close();
                                }
                            }
                        });    
                    }
                });
                //lets setup events in folderish items
                $('.panel .folder-listing .folderish').click(function(e){
                    var url = $(this).attr('href');
                    var media_type = $('input[name="media_type"]:checked');
                    MediaEmbedDialog.get_folder_listing('', url, media_type.val());
                    e.preventDefault();
                });
            }
        });
    },

    insert : function() {

        var editor = tinyMCEPopup.editor;

        tinyMCEPopup.restoreSelection();

        // Fixes crash in Safari
        if (tinymce.isWebKit){
            editor.getWin().focus();
        }
        var selected_link = $('#media-form input[name="internallink"]:checked').siblings('a');
        var href = selected_link.attr('href');

        var itype_class = selected_link.data('itype');
        if (itype_class === 'audio'){
            href = href + '?e=.mp3';
        }
        var media_width =$('#media-form input[name="media_width"]').val();
        var media_height =$('#media-form input[name="media_height"]').val();
        
        args = {
            href : href,
            'class' : itype_class + ' mceNonEditable media-link',
            style : 'width: '+media_width+'px; height: '+media_height+'px; display: block;'
        };

        el = editor.selection.getNode();

        if (el && el.nodeName === 'A') {
            editor.dom.setAttribs(el, args);
        } else {
            var media = '<div class="media"><a id="__mce_tmp" src="'+ tinyMCEPopup.getWindowArg("plugin_url") +'/img/embeb.png" href="__mce_tmp"></a></div>';
            editor.execCommand('mceInsertContent', false, media, {skip_undo : 1});
            editor.dom.setAttribs('__mce_tmp', args);
            
            editor.dom.setAttrib('__mce_tmp', 'id','');
            editor.undoManager.add();
        }
    
        // Insert the contents from the input into the document
        //tinyMCEPopup.editor.execCommand('mceInsertContent', false, $('#media-form input[name="internallink"]:checked').siblings('a').attr('href'));
        tinyMCEPopup.close();
    }
};

tinyMCEPopup.onInit.add(MediaEmbedDialog.init, MediaEmbedDialog);
