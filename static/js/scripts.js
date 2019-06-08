$.ajax({
    url: '/blog/comments/add/',
    type: 'POST',
    data: { post_id: 12, text: 'Занятная идея!' },
}).success(function(data) {
    if (data.status == 'ok') {
        console.log(data.comment_id);
    }
}).error(function() {
    console.log('http error')
});

