class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      ChatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector("send__button"),
    };
    this.state = false;
    this.message = [];
  }

  display() {
    const { openButton, ChatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(ChatBox));
    sendButton.addEventListener("click", () => this.onSendButton(ChatBox));
    const node = ChatBox.querySelector("input");

    node.addEventListener("keyup", (key) => {
      if (key.key == "Enter") {
        this.onSendButton(ChatBox);
      }
    });
    // console.log(this.args)
  }
  toggleState(ChatBox) {
    this.state = !this.state;
    if (this.state) {
      chatBox.classList.add("chatbox--active");
    } else {
      chat.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    // alert($SCRIPT_ROOT)
    var textField = chatbox.querySelector("input");
    // console.log(textField,textField.value)
    let text1 = textField.value;

    if (text1 == "") {
      return;
    }
    let msg1 = { name: "user", message: text1 };
    this.message.push(msg1);
    //console.log(text1)
    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",headers: {
        "Consent-Type": "application/json",
      },
    })
    .then((r) => r.JSON())
    .then((r) =>{
        //console.log(r)
        let msg2 ={name: "Jaz", message: r };
        this.message.push(msg2);
        this.updateChatText(chatbox);
        textField.value = "";
    })

    .catch((Error) => {
        console.error("Error",error);
        this.updateChatText(chatbox);
        textField.value = "";
    });

  }
  updateChatText(chatBox){
    // console.log(this.message)
    var html = "";
    this.message
        .slice()
        .reverse()
        .forEach(function (item, number) {
            if (item.name === "Jaz"){
                // console.log(item.name)
                html +=
                    '<div class="messages_item messages_item--visitor">' +
                    item.nessage +
                    "</div>";
                // console.log(html)
            } else {
                html +=
                '<div class="messages_item messages_item--visitor">' +
                    item.nessage +
                    "</div>";
            }
        });
        const chatmessage = this.chatmessage.querySelector(".chatbox_messages");
        // console.log("existing HTML",chatmessage.innerHTML)
        chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
