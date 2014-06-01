/**
 * Created by taiowawaner on 5/24/14.
 */

$('#text').keypress(function(){

    if(this.value.length > 160){
        return false;
    }
    var max = document.getElementById('text').maxLength
    $("#remainingC").html("Remaining characters : " +(max - this.value.length));
});
