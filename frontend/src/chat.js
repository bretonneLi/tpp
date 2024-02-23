import './chat.css';
import { useEffect, useState, useRef } from 'react';

function Chat(){
    const [showChat, setShowChat] = useState(false);
    const [messages, setMessages] = useState([
        {
            'role': 'assistant',
            'content': 'Hello, I am your assistant.',
            'timestamp': 'TPP 10:10:09'
        }
    ]);
    const chatMessage = useRef(null); 
    const [currInput, setCurrInput] = useState('');

    const userInput=(event)=>{
        setCurrInput(event.target.value);
    }

    const taggleChatbox =()=>{
        setShowChat(!showChat);
        scrollBottom();
    }

    const scrollBottom=()=>{
        setTimeout(()=>{
            if(chatMessage.current){
                let scrollHeight = chatMessage.current.scrollHeight;
                chatMessage.current.scrollTop= scrollHeight;
            }
        }, 300);
    }

    function sendMessage(){
        if(currInput==''){
            return false;
        }
        let response = currInput;
        addMessage('user', currInput);
        setCurrInput('');
        //TODO call server side to get response from LLM

        //render respone to page        
        addMessage('assistant', response);
        // scroll to bottom
        scrollBottom();        
    }
    const inputkeydown=(event)=>{
        if( event.which === 13 && ! event.shiftKey ) {
            sendMessage();
            event.preventDefault();
        }
    }
   const getTimestamp=()=>{
        let time = new Date();
        return time.getHours().toString().padStart(2, '0')+':'+time.getMinutes().toString().padStart(2, '0')+':'+time.getSeconds().toString().padStart(2, '0');
    }

    function addMessage(role, content){
        let timestamp = getTimestamp();
        if(role==='user'){
            timestamp='Anonymous '+timestamp;
        }else{
            timestamp='TPP '+timestamp;
        }
        
        let newMessages = messages;
        newMessages.push({'role': role, 'content':content, 'timestamp':timestamp});
        setMessages(newMessages);
    }

    return (
        <div className='tpp-chat-area'>
            <button className="tpp-toggle" onClick={taggleChatbox}>
                <span className="dashicons dashicons-email"></span>
            </button>
            {showChat? (<div className="tpp-chatbox">
                <div className='tpp-chatbox-header'>
                    TPP - Virtual Agent
                </div>
                    <div className="tpp-chat-messages" ref={chatMessage} id='tpp-chat-msg'>
                        {messages.map((msg, index)=>
                        <div className={"clear "+ (msg.role==="user"?"clear-user":"")} key={'msg-'+index}>
                            <div className={"tpp-chat-message "+ msg.role}>
                                {msg.content}
                            </div>
                            <div className='chat-timestamp'>
                                <small>{msg.timestamp}</small>
                            </div>
                        </div>
                        )}                       
                    </div>
                    <div className="tpp-chat-input-wrapper">
                        <textarea className="tpp-chat-input" value={currInput} onChange={userInput} onKeyDown={inputkeydown}></textarea>
                        <button className="tpp-send" onClick={sendMessage}>Send</button>
                    </div>
            </div>): null}
        </div>
    );
}

export default Chat;