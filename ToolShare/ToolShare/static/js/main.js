
function openCity(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

jQuery(document).ready(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='RegistrationForm']").validate({
    // Specify validation rules
    rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        first_name: {required: true, maxlength: 30},
        last_name: {required: true, maxlength: 30},
        email:{required: true, email: true},
        username: {required: true, minlength:2},
        password:{required: true, maxlength:20},
        confirmpass: {required: true, equalTo: "#password", maxlength:20},
        address_line1: {required: true, maxlength: 100},
        state:{required: true, maxlength: 30},
        city:{required: true, maxlength: 100},
        zip:{required: true, maxlength: 30},
        phone_no:{required: true, maxlength: 15},
    },
    messages: {
        first_name: {required:"Please enter your Firstname", maxlength: "Your Firstname must consist of maximum 30 characters"},
        last_name: {required:"Please enter your Lastname", maxlength: "Your Lastname must consist of maximum 30 characters"},
        email: {email:"Enter valid Email", required: "Please enter your Email"},
        username: {minlength: "Your Username must consist of atleast 2 characters", required: "Enter your Username"},
        password: {required: "Enter your Password", maxlength:"Your Password must consist of maximum 20 characters"},
        confirmpass: {required: "Enter your confirm Password", equalTo: "Enter same password as above", maxlength:"Your Password must consist of maximum 20 characters"
        },
        address_line1:{required:"Please enter your Address Line1", maxlength: "Your Address line1 must consist of maximum 100 characters"},
        state: {required:"Please enter your State", maxlength: "Your State must consist of maximum 30 characters"},
        city:{required:"Please enter your City", maxlength: "Your City must consist of maximum 100 characters"},
        zip:{required:"Please enter your Zip", maxlength: "Your Zip must consist of maximum 30 characters"},
        phone_no:{required:"Please enter your Telephone", maxlength: "Your Telephone must consist of maximum 15 characters"},
    }
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
  })
});
