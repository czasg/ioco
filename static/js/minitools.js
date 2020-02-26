function autoAdaptIframeHeight(iframe) {
    if (iframe) {
        var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
        if (iframeWin.document.body) {
            iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
        }
    }
};

function copyText(text){
    const textarea = document.createElement("textarea")
    textarea.value = text
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand("copy")
    textarea.remove()
}

class Logger{
    alert(...args){alert(...args)}
    log(...args){console.log(...args)}
    debug(...args){console.debug(...args)}
    info(...args){console.info(...args)}
    warn(...args){console.warn(...args)}
    error(...args){console.error(...args)}
}

class AlertWindow{
    constructor(show="fast", fadeOut="normal"){
        this.show = show
        this.fadeOut = fadeOut
        this.cssStyle = {
            'position': 'fixed',
            'z-index': '9999',
            'padding': '10px',
            'border-radius': '5px',
            'min-width': '200px',
            'text-align': 'center',
            'left': '50%',
            'top': '10%',
            'transform': 'translate(-50%, -50%)',
            'display': 'none',
            'color': '#fff',
        }
    }
    alert(msg, bgColor, delay=1200){
        let div = $('<div>')
            .css(this.cssStyle)
            .css('backgroundColor', bgColor)
            .appendTo('body');
        div.html(msg).show(this.show).delay(delay);
        div.fadeOut(this.fadeOut, () => div.remove());
    }
    info(msg, delay=1200, bgColor='#9CCC65'){
        if (!msg) return
        this.alert(msg, bgColor, delay)
    }
    error(msg, delay=1200, bgColor='#EF5350'){
        if (!msg) return
        this.alert(msg, bgColor, delay)
    }
}

class MiniRandom{
    constructor(){
        this.symbols = '~!@#$%^&*()_+{}":?><;.,'
        this.randomType = {
            lower: true,
            upper: true,
            int: true,
            symbol: false
        }
    }
    _charCode(type, position){
        return String.fromCharCode(Math.floor(Math.random() * type) + position);
    }
    _rangeRandom(length){
        return Math.floor(Math.random() * length)
    }
    arrayRandom(obj){
        return obj[this._rangeRandom(obj.length)]
    }
    lower(){return this._charCode(26, 97)}
    upper(){return this._charCode(26, 65)}
    int(){return this._charCode(10, 48)}
    symbol(){return this.arrayRandom(this.symbols)}
    random(length){
        if (!length) return ''
        let results = '', types = [];
        for (let type in this.randomType){
            if (this.randomType[type] === true){
                types.push(type)
            }
        }
        for (let i = 0; i < length; i++){
            results += this[this.arrayRandom(types)]()
        }
        return results
    }
}
