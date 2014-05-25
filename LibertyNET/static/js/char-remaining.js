function charRemaining(txtarea, uparear)
{
    var x=document.getElementById(txtarea);
    var ml = x.maxLength;
    var rm = ml - x.value.length;
    var hashstr = '#';
    var upelem = hashstr.concat(uparear);
    var func_str = hashstr.concat(txtarea.toString());
    $(func_str).keypress(function(){
                        if(this.value.length > ml){
                            return false;
                        }
    });
    $(upelem).html(rm);
}

function initialChar(txtarea, uparea) {
    var txt = document.getElementById(txtarea);
    var max = txt.maxLength;
    var rm = max - txt.value.length;
    var hash = '#'.concat(uparea);
    $(hash).html("Characters Remaining: " + (rm));

}

function get_remaining_char(txtId) {
    var txt = document.getElementById(txtId);
    var rem = (txt.maxLength - txt.value.length).toString();
    return rem
}