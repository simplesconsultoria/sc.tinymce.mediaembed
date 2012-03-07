tinyMCEPopup.requireLangPack();

var TemplateDialog = {
    preInit : function() {
        
        // Use this parameter to load another JavaScript file with template
        // definitions. By default, we load our own list using the semantics
        // described in the README.
        var url = tinyMCEPopup.getParam("template_external_list_url");

        if (url != null)
            document.write('<sc'+'ript language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></sc'+'ript>');
    },

    init : function() {
        var ed = tinyMCEPopup.editor, tsrc, sel, x, u;
        
        
        // Load templates from an explicit parameter. By default, we don't
        // use this
        tsrc = ed.getParam("template_templates", false);
        sel = document.getElementById('tpath');

        // Use external template list as a fallback
        if (!tsrc && typeof(tinyMCETemplateList) != 'undefined') {
            for (x=0, tsrc = []; x<tinyMCETemplateList.length; x++)
                tsrc.push({title : tinyMCETemplateList[x][0], src : tinyMCETemplateList[x][1], description : tinyMCETemplateList[x][2]});
        }

        for (x=0; x<tsrc.length; x++)
            sel.options[sel.options.length] = new Option(tsrc[x].title, tinyMCEPopup.editor.documentBaseURI.toAbsolute(tsrc[x].src));

        this.resize();
        this.tsrc = tsrc;
    },

    resize : function() {
        var w, h, e;

        if (!self.innerWidth) {
            w = document.body.clientWidth - 50;
            h = document.body.clientHeight - 160;
        } else {
            w = self.innerWidth - 50;
            h = self.innerHeight - 170;
        }
        
        e = document.getElementById('templatesrc');

        if (e) {
            e.style.height = Math.abs(h - 80) + 'px';
            e.style.width  = Math.abs(w - 100) + 'px';
        }
    },

    loadCSSFiles : function(d) {
        var ed = tinyMCEPopup.editor;

        tinymce.each(ed.getParam("content_css", '').split(','), function(u) {
            d.write('<link href="' + ed.documentBaseURI.toAbsolute(u) + '" rel="stylesheet" type="text/css" />');
        });
    },

    selectTemplate : function(u, ti) {
        var d = window.frames['templatesrc'].document, x, tsrc = this.tsrc;

        if (!u)
            return;

        d.body.innerHTML = this.templateHTML = this.getFileContents(u);

        for (x=0; x<tsrc.length; x++) {
            if (tsrc[x].title == ti)
                document.getElementById('tmpldesc').innerHTML = tsrc[x].description || '';
        }
    },

    insert : function() {
        tinyMCEPopup.execCommand('mcePloneInsertTemplate', false, {
            content : this.templateHTML,
            selection : tinyMCEPopup.editor.selection.getContent()
        });

        tinyMCEPopup.close();
    },

    getFileContents : function(u) {
        var x, d, t = 'text/plain';

        function g(s) {
            x = 0;

            try {
                x = new ActiveXObject(s);
            } catch (s) {
            }

            return x;
        };

        x = window.ActiveXObject ? g('Msxml2.XMLHTTP') || g('Microsoft.XMLHTTP') : new XMLHttpRequest();

        // Synchronous AJAX load file
        x.overrideMimeType && x.overrideMimeType(t);
        x.open("GET", u, false);
        x.send(null);

        return x.responseText;
    }
};

TemplateDialog.preInit();
tinyMCEPopup.onInit.add(TemplateDialog.init, TemplateDialog);
