$ () ->

    # initial state - disable forgot password input
    $('#forgot-password input').attr('disabled', true)

    $('#login a.switch-state').click (event) ->
        event.preventDefault()        
        $('.state').toggleClass 'hide'
        $('.state input').attr('disabled', false)
        $('.state.hide input').attr('disabled', true)

    $('#login .btn').click(Datafly.submit)
