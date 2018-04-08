const chatRoom = document.querySelector('.row').dataset.chatRoom;
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatRoom}/`);

const renderMessage = ((user, message, datetime) => {
  const html = `<div class="alert alert-primary msg" role="alert">
    <h6 class="alert-heading username">${user}<span class="time" style="float: right">${datetime}</span></h6>
    <hr>
    <p class="mb-0 text">${message}</p>
  </div>`;
  const messagesHtml = document.querySelector('.messages');
  messagesHtml.insertAdjacentHTML('beforeend', html);
});

chatSocket.onmessage = ((e) => {
  const data = JSON.parse(e.data);
  const user = data['message_sender'];
  const message = data['message_text'];
  const datetime = data['message_send_datetime'];
  renderMessage(user, message, datetime);
});

chatSocket.onclose = ((e) => {
  console.error('Chat socket closed unexpectedly');
});

const sendMessage = ((e) => {
  const messageInputDom = document.querySelector('#message-text');
  const message = messageInputDom.value;
  const user = document.querySelector('.row').dataset.user;
  chatSocket.send(JSON.stringify({
    'message_sender': user,
    'message_text': message
  }));

  messageInputDom.value = '';
});

document.querySelector('#message-submit').onclick = sendMessage;
