var current_menu = "inbox"
document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  //history.pushState({ section: "compose" }, "", `/`);

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields~
  let compose_recipients = document.querySelector('#compose-recipients')
  let compose_subject = document.querySelector('#compose-subject')
  let compose_body = document.querySelector('#compose-body')

  compose_recipients.value = '';
  compose_subject.value = '';
  compose_body.value = '';
  console.log("this is one time");
  document.querySelector('#compose-form').addEventListener('submit', () => {
    console.log("submitted")

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: compose_recipients.value,
        subject: compose_subject.value,
        body: compose_body.value
      })
    })
      .then(response => response.json())
      .then(result => {
        // Print result
        console.log(result);
      });
  });
}

function load_mailbox(mailbox) {
  //history.pushState({section: mailbox}, "", `/emails/${mailbox}`);
  current_menu = mailbox
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-list').innerHTML = '';
  document.querySelector('.layout-container2').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-type').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach((email) => {
        let mail_component = document.querySelector('.mail-container')
        clone_mail = mail_component.cloneNode(true)
        clone_mail.querySelector('.mail-link').addEventListener('click', () => view_mail(email))
        clone_mail.querySelector('.mail-subject').innerHTML = email.subject
        clone_mail.querySelector('.mail-time').innerHTML = email.timestamp
        clone_mail.querySelector('.mail-from').innerHTML = "from: " + email.sender
        if (mailbox === "sent") {
          clone_mail.querySelector('.mail-from').innerHTML = "sent to: " + email.recipients
        }
        clone_mail.style.display = "block"
        if (email.read === true) {
          clone_mail.style.background = "grey";
        }
        document.querySelector('#emails-list').appendChild(clone_mail)
      })
      // ... do something else with emails ...
    });
}

function view_mail(email) {
  // Display layout for email
  let layout_container2 = document.querySelector('.layout-container2');
  layout_container2.style.display = 'block';
  layout_container2.innerHTML = '';

  // Load email content
  let mail_component = document.querySelector('.mail-container2')
  let clone_mail = mail_component.cloneNode(true)
  clone_mail.style.display = 'block';
  clone_mail.querySelector('.mail-subject').innerHTML = "Subject: " + email.subject
  clone_mail.querySelector('.mail-from').innerHTML = "from: " + email.sender
  clone_mail.querySelector('.mail-to').innerHTML = "to: " + email.recipients
  clone_mail.querySelector('.mail-time').innerHTML = email.timestamp
  clone_mail.querySelector('.mail-body').innerHTML = email.body

  // Archive email
  let archive = true
  clone_mail.querySelector('.mail-archive').innerHTML = "Archive"
  clone_mail.querySelector('.mail-archive').style.background = 'grey'
  clone_mail.querySelector('.mail-archive').style.color = 'white'
  if (email.archived === true) {
    clone_mail.querySelector('.mail-archive').innerHTML = "Archived"
    clone_mail.querySelector('.mail-archive').style.background = 'cyan'
    archive = false
  }
  const archive_email = () => {
    fetch('/emails/' + email.id, {
      method: 'PUT',
      body: JSON.stringify({
        archived: archive
      })
    }).then(() => {
      
      if (archive === false) {
        load_mailbox('archive')
      } else {
        load_mailbox('inbox')
      }
      clone_mail.querySelector('.mail-archive').removeEventListener('click', archive_email)
    })
  }
  if (current_menu !== "sent") {
    clone_mail.querySelector('.mail-archive').addEventListener('click', archive_email)
  } else{
    clone_mail.removeChild(clone_mail.querySelector('.mail-archive'))
  }
  

  // Replay email
  const reply_email = () => {
    // Copy of compose_email function
    //history.pushState({ section: "compose" }, "", `/`);
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    let compose_recipients = document.querySelector('#compose-recipients')
    let compose_subject = document.querySelector('#compose-subject')
    let compose_body = document.querySelector('#compose-body')
  
    compose_recipients.value = email.sender;
    compose_subject.value = 'Re: '+email.subject;
    compose_body.value = 'On '+email.timestamp+" "+email.sender+" wrote: "+email.body;
  
    document.querySelector('#compose-form').addEventListener('submit', () => {
      console.log("submitted")
   
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: compose_recipients.value,
          subject: compose_subject.value,
          body: compose_body.value
        })
      })
        .then(response => response.json())
        .then(result => {
          console.log(result);
        });
    });
  }
  clone_mail.querySelector('.mail-reply').addEventListener('click', reply_email)

  // Update read email
  fetch('/emails/' + email.id, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  layout_container2.appendChild(clone_mail)
}

