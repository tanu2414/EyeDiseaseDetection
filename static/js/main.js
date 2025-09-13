

(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    

    $('.validate-form').on('submit',function(){
        var fid=$(this).attr('id');
        var input = $('.'+fid);
        var check = true;
        var isErr=false;
        for(var i=0; i<input.length; i++) {
            console.log(input[i]);
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
                isErr=true;
            }
        }
        console.log(fid+","+isErr +","+ check);
        checkLogin(fid,isErr);
        return false;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else if($(input).attr('name') == 'rpass2') {
            let pass=$("#passr").val();
            if($(input).val() != pass){
                return false;
            }
        }else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);