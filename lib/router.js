Router.route('/upload', {name: 'upload'});

Router.route('/results', {name: 'result'});

Router.configure({
  notFoundTemplate: 'not_found',
  loadingTemplate: 'spinner',
});
