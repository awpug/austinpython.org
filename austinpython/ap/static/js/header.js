var Header = {

    CURRENT_MODULE: 0,
    ELEMENT_ID: "#module",
    ELEMENT: null,
    UNDERSCORE: false,
    UPDATING: false,
    WORD_INTERVAL: 6000,
    LETTER_INTERVAL: 75,
    CURSOR_INTERVAL: 500,

    MODULES: [
        "django", "numpy", "sqlalchemy", "pygtk", "fabric", "Image",
        "vtk", "Crypto", "pychem", "twisted", "this", "flask", "Tkinter",
        "requests", "markdown", "unittest2", "tornado", "twisted",
        "oauth2", "gevent"
    ],

    init: function() {
        Header.ELEMENT = $(Header.ELEMENT_ID);
        setInterval(Header.word_callback, Header.WORD_INTERVAL);
        setInterval(Header.underscore_callback, Header.CURSOR_INTERVAL);
        // staring with initial module
        Header.seed_module();
        Header.ELEMENT.text("");
        Header.add_letter();
    },

    seed_module: function() {
        var index;
        do {
            index = Math.floor(Math.random() * Header.MODULES.length);
        } while (index == Header.CURRENT_MODULE);
        Header.CURRENT_MODULE = index;
        return index;
    },

    word_callback: function() {
        if (Header.UPDATING)
            return;
        Header.UPDATING = true;
        Header.remove_letter();
    },

    remove_letter: function() {
        var text = Header.ELEMENT.text();
        var length = Header.get_length();
        if (length <= 0)
            return Header.add_letter();
        var new_text = text.substring(0, length-1);
        if (Header.UNDERSCORE)
            new_text += "_";
        Header.ELEMENT.text(new_text);
        setTimeout(Header.remove_letter, Header.LETTER_INTERVAL);
    },

    add_letter: function() {
        var module = Header.MODULES[Header.CURRENT_MODULE];
        var text = Header.ELEMENT.text();
        var length = Header.get_length();
        if (length >= module.length) {
            Header.seed_module();
            if (Header.CURRENT_MODULE >= Header.MODULES.length)
                Header.CURRENT_MODULE = 0;
            Header.UPDATING = false;
            return;
        }
        var new_text = module.substring(0, length+1);
        if (Header.UNDERSCORE)
            new_text += "_";
        Header.ELEMENT.text(new_text);
        setTimeout(Header.add_letter, Header.LETTER_INTERVAL);
    },

    get_length: function() {
        var text = Header.ELEMENT.text();
        var length = text.length;
        if (Header.UNDERSCORE)
            length -= 1;
        return length;
    },

    underscore_callback: function() {
        var text = Header.ELEMENT.text();
        if (text.match(/_$/)) {
            Header.UNDERSCORE = false;
            Header.ELEMENT.text(text.substring(0, text.length - 1));
        } else {
            Header.UNDERSCORE = true;
            Header.ELEMENT.text(text+"_");
        }
    }

};
