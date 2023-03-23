$(document).ready(function(){
    var zoom = 1 ;
    var zoomStep = 0.1;

    if(localStorage.getItem("contrast") == "highcontrast"){
        $("body").attr("class", "highcontrast");
        $(".container .section nav").removeClass("bg-light");
    }

    if(localStorage.getItem("zoom") == null){
        localStorage.setItem("zoom", zoom);
    }
    else{
        document.body.style.zoom = parseFloat(localStorage.getItem("zoom"));
    }

    if(localStorage.getItem("zoom") == null){
        localStorage.setItem("zoom", zoom);
    }

    $("#selectstart").on("change", function (e) {
        if ($(this).val() != ""){
            var address = $('option:selected',this).data("address");
            var postcode = $('option:selected',this).data("postcode");

            $("#start").val(address);
            $("#postcode").val(postcode);
        }
        else{
            $("#start").val("");
            $("#postcode").val("");
        }
    });

    $("#selectend").on("change", function (e) {
        if ($(this).val() != ""){
            var address = $('option:selected',this).data("address");
            var postcode = $('option:selected',this).data("postcode");

            $("#end").val(address);
            $("#endpostcode").val(postcode);
        }
        else{
            $("#end").val("");
            $("#endpostcode").val("");
        }
    });

    $("#submitlogin").on('click', function(e) {
        e.preventDefault();
        $(".alert, .text-danger").hide();
        var username = $("#username").val();
        var password = $("#password").val();
        var valid = true;
        if (username == ""){
            valid = false;
            $("#username").after("<strong class='text-danger'>Please enter username</strong>");
            $("#username").addClass("is-invalid");
        } else{ $("#username").removeClass("is-invalid"); $("#username").addClass("is-valid"); }
        if (password == ""){
            valid = false;
            $("#password").after("<strong class='text-danger'>Please enter password</strong>");
            $("#password").addClass("is-invalid");
        } else{ $("#password").removeClass("is-invalid"); $("#password").addClass("is-valid"); }
        if(valid){
            $.ajax({
                data: $("#loginform").serialize(),
                url: $("#loginform").attr("action"),
                method: "POST",
                type: "text",
                success: function(res) {
                    if (res == "success"){
                        $("#loginform").before("<div class='alert alert-success'>Login Successful</div>");
                        setTimeout(function() {
                            window.location = "/getroute";
                        }, 2000);
                        
                    }
                    else{
                        $("#loginform").before(res);
                    }
                },
                
            });
        }
    });

    $("#changeusernameform").on('submit', function(e) {
        e.preventDefault();
        $(".alert").hide();
        var form = $("#changeusernameform");
        var username = $("#changeusername").val();
        var valid = true;
        if (username == ""){
            valid = false;
            $(form).before("<div class='alert alert-danger'>Please enter a username</div>");
        }
        if(valid){
            $.ajax({
                data: $(form).serialize(),
                url: $(form).attr("action"),
                method: "POST",
                type: "text",
                success: function(res) {
                    if (res == "success"){
                        $(form).before("<div class='alert alert-success'>Successfully updated</div>");
                        
                        setTimeout(function() {
                            window.location.reload();
                        }, 2000);
                    }
                    else{
                        $(form).before(res);
                    }
                },
                
            });
        }
        setTimeout(function() {
            $(".alert").hide("slow");
        }, 2000);
    });

    $("#changepasswordform").on('submit', function(e) {
        e.preventDefault();
        $(".alert").hide();
        var form = $("#changepasswordform");
        var oldpassword = $("#oldpassword").val();
        var newpassword = $("#newpassword").val();
        var valid = true;
        if (oldpassword == ""){
            valid = false;
            $(form).before("<div class='alert alert-danger'>Please enter a password</div>");
        }
        if (newpassword == ""){
            valid = false;
            $(form).before("<div class='alert alert-danger'>Please enter a password</div>");
        }
        if(valid){
            $.ajax({
                data: $(form).serialize(),
                url: $(form).attr("action"),
                method: "POST",
                type: "text",
                success: function(res) {
                    if (res == "success"){
                        $(form).before("<div class='alert alert-success'>Successfully updated</div>");
                        
                        setTimeout(function() {
                            window.location.reload();
                        }, 2000);
                    }
                    else{
                        $(form).before(res);
                    }
                },
                
            });
        }
        setTimeout(function() {
            $(".alert").hide("slow");
        }, 2000);
    });

    $("#showsavejourney").on("click", function(e) {
        $(".saveaddress").toggle('slow');
        $("#savejourney").show();
    });

    $("#resetzoom").on("click", function(e) {
        document.body.style.zoom=1.0;
        localStorage.clear();
    });

    $("#zoomin").on("click", function(e) {
        
        var currentZoom = zoom;
        if(localStorage.getItem("zoom") != null){
            currentZoom = parseFloat(localStorage.getItem("zoom"));
        }
        currentZoom += zoomStep;
        document.body.style.zoom = currentZoom;
        localStorage.setItem("zoom", currentZoom);
    });

    $("#zoomout").on("click", function(e) {
        
        var currentZoom = zoom;
        if(localStorage.getItem("zoom") != null){
            currentZoom = parseFloat(localStorage.getItem("zoom"));
        }
        currentZoom -= zoomStep;
        document.body.style.zoom = currentZoom;
        localStorage.setItem("zoom", currentZoom);
    });

    $("#getroute").on("click", function (e) {
        $(".alert").hide();
        $(".text-danger").hide();
        var start = $("#start").val();
        var end = $("#end").val();
        var postcode = $("#postcode").val();
        var endpostcode = $("#endpostcode").val();
        var valid = true;
        if (start == ""){
            valid = false;
            $("#start").after("<strong class='text-danger'>Please enter an address</strong>");
            $("#start").addClass("is-invalid");
        } else{ $("#start").removeClass("is-invalid"); $("#start").addClass("is-valid"); }

        if (end == ""){
            valid = false;
            $("#end").after("<strong class='text-danger'>Please enter an address</strong>");
            $("#end").addClass("is-invalid");
        } else{ $("#end").removeClass("is-invalid"); $("#end").addClass("is-valid"); }

        if ((endpostcode == "") || (endpostcode.match(/[\S]{1,2}[\d]{1,2}[\S]?\ ?[\d]{1,2}[\S]{1,2}/)==null)){
            valid = false;
            $("#endpostcode").after("<strong class='text-danger'>Please enter a valid postcode</strong>");
            $("#endpostcode").addClass("is-invalid");
        } else{ $("#endpostcode").removeClass("is-invalid"); $("#endpostcode").addClass("is-valid"); }

        if ((postcode == "") || (postcode.match(/[\S]{1,2}[\d]{1,2}[\S]?\ ?[\d]{1,2}[\S]{1,2}/)==null)){
            valid = false;
            $("#postcode").after("<strong class='text-danger'>Please enter a valid postcode</strong>");
            $("#postcode").addClass("is-invalid");
        } else{ $("#postcode").removeClass("is-invalid"); $("#postcode").addClass("is-valid"); }

        if (valid){
            $("#mapframe").before("<label class='alert alert-info'>Loading route, please wait...</label>");
            $.ajax({
            data: $("#journeyform").serialize(),
            url: $("#journeyform").attr("action"),
            method: "POST",
            type: "text",
            success: function (res) {
                if (res == "success") {
                    document.getElementById("mapframe").contentDocument.location.reload(true);
                    $(".alert").hide();
                    $("#mapframe").before("<label class='alert alert-success'>Route Loaded</label>");
                }
            },

        });
        }
        
    });

    $("#savejourney").on("click", function (e) {
        $(".alert").hide();
        $(".text-danger").hide();
        var start = $("#start").val();
        var end = $("#end").val();
        var postcode = $("#postcode").val();
        var endpostcode = $("#endpostcode").val();
        var startname = $("#startname").val();
        var endname = $("#endname").val();
        var journeyName = $("#journeyName").val();
        var valid = true;
        if (start == ""){
            valid = false;
            $("#start").after("<strong class='text-danger'>Please enter an address</strong>");
            $("#start").addClass("is-invalid");
        } else{ $("#start").removeClass("is-invalid"); $("#start").addClass("is-valid"); }

        if (end == ""){
            valid = false;
            $("#end").after("<strong class='text-danger'>Please enter an address</strong>");
            $("#end").addClass("is-invalid");
        } else{ $("#end").removeClass("is-invalid"); $("#end").addClass("is-valid"); }

        if ((endpostcode == "") || (endpostcode.match(/[\S]{1,2}[\d]{1,2}[\S]?\ ?[\d]{1,2}[\S]{1,2}/)==null)){
            valid = false;
            $("#endpostcode").after("<strong class='text-danger'>Please enter a valid postcode</strong>");
            $("#endpostcode").addClass("is-invalid");
        } else{ $("#endpostcode").removeClass("is-invalid"); $("#endpostcode").addClass("is-valid"); }

        if ((postcode == "") || (postcode.match(/[\S]{1,2}[\d]{1,2}[\S]?\ ?[\d]{1,2}[\S]{1,2}/)==null)){
            valid = false;
            $("#postcode").after("<strong class='text-danger'>Please enter a valid postcode</strong>");
            $("#postcode").addClass("is-invalid");
        } else{ $("#postcode").removeClass("is-invalid"); $("#postcode").addClass("is-valid"); }

        if (startname == ""){
            valid = false;
            $("#startname").after("<strong class='text-danger'>Please enter an address name</strong>");
            $("#startname").addClass("is-invalid");;
        } else{ $("#startname").removeClass("is-invalid"); $("#startname").addClass("is-valid"); }

        if (endname == ""){
            valid = false;
            $("#endname").after("<strong class='text-danger'>Please enter an address name</strong>");
            $("#endname").addClass("is-invalid");;
        } else{ $("#endname").removeClass("is-invalid"); $("#endname").addClass("is-valid"); }

        if (journeyName == ""){
            valid = false;
            $("#journeyName").after("<strong class='text-danger'>Please enter a journey name</strong>");
            $("#journeyName").addClass("is-invalid");;
        } else{ $("#journeyName").removeClass("is-invalid"); $("#journeyName").addClass("is-valid"); }

        if (startname == endname && valid == true){
            valid = false;
            $("#startname").after("<strong class='text-danger'>Please enter two different address names</strong>");
            $("#startname").addClass("is-invalid");;
            $("#endname").addClass("is-invalid");;
        }
        if (valid){
            $.ajax({
                data: $("#journeyform").serialize(),
                url: "http://127.0.0.1:5000/savejourney",
                method: "POST",
                type: "text",
                success: function (res) {
                    if (res == "success") {
                        $(".saveaddress").toggle('slow');
                    }
                    if (res == "notUniqueJourneyName") {
                        $("#journeyName").after("<strong class='text-danger'>Journey name already in use</strong>");
                    }
                },

            });
        }
    });

    $(".deleteJourney").on("click", function (e) {
        var choice = confirm("Are you sure?");
        if (choice == true) {
            $.ajax({
            data: {'journeyid': $(this).attr('data-journeyid')},
            url: "/deletejourney",
            method: "POST",
            type: "text",
            success: function (res) {
                window.location.reload();
            }
            });
        }
        
    });

    $("#togglecontrast").on("click", function (e) {
        var current = $("body").attr("class");
        localStorage.setItem("contrast", "");
        if (current == "highcontrast"){
            localStorage.setItem("contrast", "");
            $("body").removeAttr("class");
            $(".container .section nav").addClass("bg-light");
        }
        else{
            localStorage.setItem("contrast", "highcontrast");
            $("body").attr("class", "highcontrast");
            $(".container .section nav").removeClass("bg-light");
        }
    })

    $("#emailform").on('submit', function(e) {
        e.preventDefault();
        $(".alert").hide();
        var form = $("#emailform");
        var email = $("#resetEmail").val();
        var valid = true;
        if (email == ""){
            valid = false;
            $(form).before("<div class='alert alert-danger'>Please enter an email</div>");
        }
        if(valid){
            $.ajax({
                data: $(form).serialize(),
                url: $(form).attr("action"),
                method: "POST",
                type: "text",
                success: function(res) {
                    if (res == "success"){
                        $(form).before("<div class='alert alert-success'>Password successfully reset.<br>You will receive an email containing a new password. Please use this password to login to your account.<br>Then go to the profile page and update your password.<br>Thanks!</div>");
                    }
                    else{
                        $(form).before(res);
                    }
                },
                
            });
        }
    });

    $("#submitregistration").on('submit', function(e) {
        e.preventDefault();
        $(".text-danger, .alert").hide();
        var username = $("#username").val();
        var password = $("#password").val();
        var email = $("#email").val();
        var firstName = $("#firstName").val();
        var valid = true;
        if (username == ""){
            valid = false;
            $("#username").after("<strong class='text-danger'>Please enter username</strong>");
            $("#username").addClass("is-invalid");
        } else{ $("#username").removeClass("is-invalid"); $("#username").addClass("is-valid"); }
        
        if (password == ""){
            valid = false;
            $("#password").after("<strong class='text-danger'>Please enter password</strong>");
            $("#password").addClass("is-invalid");
        } else{ $("#password").removeClass("is-invalid"); $("#password").addClass("is-valid"); }
        if (email == ""){
            valid = false;
            $("#email").after("<strong class='text-danger'>Please enter an email</strong>");
            $("#email").addClass("is-invalid");
        } else{ $("#email").removeClass("is-invalid"); $("#email").addClass("is-valid"); }
        if (firstName == ""){
            valid = false;
            $("#firstName").after("<strong class='text-danger'>Please enter your First Name</strong>");
            $("#firstName").addClass("is-invalid");
        } else{ $("#firstName").removeClass("is-invalid"); $("#firstName").addClass("is-valid"); }
        if(valid){
            $.ajax({
                data: $("#submitregistration").serialize(),
                url: $("#submitregistration").attr("action"),
                method: "POST",
                type: "text",
                success: function(res) {
                    if (res == "success"){
                        $("#submitregistration").before("<div class='alert alert-success'>Registration Successful</div>");
                        setTimeout(function() {
                            window.location = "/login";
                        }, 2000);
                        
                    }
                    else{
                        $("#submitregistration").before(res);
                    }
                },
                
            });
        }
    });

});