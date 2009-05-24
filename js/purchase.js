var get_form_fields = function(form) {
    var param = {};
    $(':input', form).each(function(i){
        var name = this.name;
        if (this.type == 'radio') {
            if (this.checked) param[name] = this.value;
        } else if (this.type == 'checkbox') {
            if (this.checked) param[name] = this.value;
        } else if (this.type == 'submit'){
            if (/selected/.test(this.className)) param[name] = this.value;
        } else {
            if (name) param[name] = this.value;
        }
        if(/notnull/.test(this.className) && this.value == ''){
            $(this).prev().addClass('errnotnull');
            param['err'] = 'notnull';
        }
    });
    return param;
}

$.post_withck = function( url, data, callback, type ) {
    if ($.isFunction(data)) {
        callback = data;
        data = {};
    }
    return $.ajax({
        type: "POST",
        url: url,
        data: $.extend(data,{ck:get_cookie('ck')}),
        success: callback,
        dataType: type
    });
}

var remote_submit_json = function(form, func, disable, action) {
    var fvalue = get_form_fields(form);
    if(fvalue['err'] != undefined) return;
    $(':submit,:input',form).attr('disabled',disable==false?0:1);
    var act = action || form.action;
    $.post_withck(act, fvalue, function(ret){
        var json = eval('('+ret+')'); func(json);
    });
}

var submit_purchase_json = function(url, purchases, func) {
    return $.ajax({
        type: "POST",
        url: url,
        data: purchases,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: func
    });
};

var init_purchase_form = function(form) {
    var btns = {}, selected = {};
    
    var select = function(tl) {
        if (btns[tl]) {
            selected[tl] = true;
            $.each(btns[tl], function(i, btn) {
                $(btn).removeClass('gract').addClass('rdact');
            });
        }
    }
    var deselect = function(tl) {
        if (btns[tl]) {
            delete selected[tl];
            $.each(btns[tl], function(i, btn) {
                $(btn).removeClass('rdact').addClass('gract');
            });
        }
    }
    var update = function() {
        var tags = $.trim(form.tags.value.toLowerCase()).split(' '), hash = {};
        $.each(tags, function(i, t){
            if (t != '') { select(t); hash[t] = true; }
        });
        for (t in selected) { if (!hash[t]) deselect(t) }
    };
    
    //update();
    $(form).submit(function() {
        var purchases = [];
        for (var item in selected) {
            var purchase = {"item":item,
                            "fallbacks":[],
                            "policy":"any"};
            purchases.push(purchase);
        }
	// XXX, replace it with a light-weight solution
	data = JSON.stringify(purchases);
        submit_purchase_json(this.action, data, function(data) {
            window.location.href = window.location.href.replace('entry', 'list');
	    return false;
        });
        return false;
    });

    $('.orderbtn', form).each(function(i){
        var tl = $(this).text().toLowerCase();
        if (btns[tl])
            btns[tl].push(this);
        else
            btns[tl] = [this];
    }).click(function(){
        var tag = $(this).text();
        var tags = $.trim(form.tags.value).split(' '), present=false, tl=tag.toLowerCase(), i;
        tags = $.grep(tags, function(t, i){
            if (t.toLowerCase() == tl) {
                deselect(tl); present=true; return false;
            } else return true;
        });
        if (!present) { tags.push(tag); select(tl); }
        var content = tags.join(' ');
        form.tags.value = (content.length > 1) ? content+' ' : content; 
        form.tags.focus();
    });
}

