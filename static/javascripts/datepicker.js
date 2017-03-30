$(function() {
    $("#datepicker").datepicker({
        dateFormat: 'M dd, yy',
        constrainInput: false,
        onSelect : function(){
            $('#dateform').submit();   
        }
    });
});
