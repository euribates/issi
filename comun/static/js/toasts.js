"use strict";

var toastDefaultConfig = {
    autoDismiss: true,
    container: '#toasts',
    autoDismissDelay: 6000,
    transitionDuration: 500,
    counter: 0,
};


function show_toast(message, config={}) {
    toastDefaultConfig.counter++;
    config = jQuery.extend({}, toastDefaultConfig, config);
    var close = '&times;'; // show "x"
    // toast template
    var toast = jQuery([
      '<div class="toast ' + message.tags + '">',
      '<p>' + message.message + '</p>',
      '<div class="close">' + close + '</div>',
      '</div>'
    ].join(''));
    
    // handle dismiss
    toast.find('.close').on('click', function(){
      var toast = jQuery(this).parent();
      toast.addClass('hide');
      setTimeout(
          function() { toast.remove(); },
          config.transitionDuration
      );
    });
    
    // append toast to toasts container
    jQuery(config.container).append(toast);
    
    // transition in
    setTimeout(function(){
      toast.addClass('show');
    }, config.transitionDuration);

    // if auto-dismiss, start counting
    if (config.autoDismiss) {
      setTimeout(
          function () { toast.find('.close').click(); },
          config.autoDismissDelay + (config.counter*1500)
      );
    }
    return toast;
}
