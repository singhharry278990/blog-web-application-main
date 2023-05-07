$(document).ready(function(){
  $('input[type="checkbox"]').on('change', function(){
    var username = $(this).val();
    var isChecked = $(this).is(':checked');
    updateSuspendedStatus(username, isChecked);
    console.log(username, isChecked)
  });
});
function updateSuspendedStatus(username, isChecked ) {
  $.ajax({
    url: '/suspened/', // Update the URL here to match your Django view URL
    type: 'POST',
    data: {
      'email_list': username,
      'is_on': isChecked,
      'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
    },
    success: function(data) {
      console.log(data); 
      messageElement.innerHTML = data.message;
      userElement.innerHTML = data.username;
      emailElement.innerHTML = data.Email;
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log(textStatus, errorThrown);
    }
  });
}

