document.addEventListener('DOMContentLoaded', function() {
    // by default load reminders
    load_reminders()
    // everytime we click the new reminder button we refresh the reminders might not work tho
    // document.querySelector('#new_reminder_button').addEventListener('click',() => load_reminders());

});

// write functions here 

function load_reminders(){
    
    // fetch reminders
    fetch('/api/reminders') // this is fetching it correctly
    .then(response => response.json())
    .then(reminders =>{
        console.log("hiiiii")
        console.log(reminders)
        // do something with reminders
        // cant reinitialise a datatable
        $('#user_reminders_table').DataTable({
            data : reminders,
            columns: [
                { data : 'reminder_name'},
                { data : 'reminder_description'},
                { data : 'reminder_start_date'}
                
            ]
        })

        


    })
};

function new_reminder(){
    
}

