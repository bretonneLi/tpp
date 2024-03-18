import './chatbot.css';
import {retriver,chatInit,getCurrentLLM} from './api/chat';
import { useEffect, useState, useRef } from 'react';

function Chatbot(){
    const getTimestamp=()=>{
        let time = new Date();
        return time.getHours().toString().padStart(2, '0')+':'+time.getMinutes().toString().padStart(2, '0')+':'+time.getSeconds().toString().padStart(2, '0');
    }
    const [currentLLM, setCurrentLLM] = useState('');
    const [showChat, setShowChat] = useState(false);
    const [messages, setMessages] = useState([
        // {
        //     'role': 'init',
        //     'content': 'Hello, I am your assistant.',
        //     'timestamp': 'TPP '+ getTimestamp(),
        //     'items': [
        //         'Weclome.',
        //         'I am TPP Agent and I only answer in English and French',
        //         'Select a topic in the below list or ask me directly your question.'
        //     ]
        // }
    ]);

    useEffect(()=>{
        initChatbot();
        getLLM();
    }, []);

    async function getLLM(){
        getCurrentLLM().then((response)=>{
            // console.log(response);
            setCurrentLLM(response.data.llm_name);
        }).catch((error)=>{
            console.log(error);
        });
    }

    async function initChatbot(){
        chatInit().then((response)=>{
            console.log(response);
            if(response&&response.data){
                let timestamp = getTimestamp();
                // 单条更新
                setMessages([...messages, {'role': 'init', 'content':'', 'timestamp':'TPP '+timestamp, 'items': response.data}]);
            }            
        }).catch((error)=>{
            console.log('error initing chatbot: '+ error);
        });
    }

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
        let question = currInput;
        addMessage('user', currInput);   
        setCurrInput('');  
        // start blink   
        setMessages([...messages, {'role': 'calling', 'content':'', 'timestamp': ''}]);
        // scroll to bottom
        scrollBottom();
        //call server side to get response from LLM
        retriver(question, currentLLM).then((response)=>{
            console.log(response.data);
            if(response&&response.data){
                let timestamp = getTimestamp();
                //render respone to page
                addMessage('assistant', response.data.result);
                // scroll to bottom
                scrollBottom();
            }
        }).catch((error)=>{
            console.log('retriver failed with error: '+error);
        });
    }

    const inputkeydown=(event)=>{
        if( event.which === 13 && ! event.shiftKey ) {
            sendMessage();
            event.preventDefault();
        }
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
        // 单条更新
        // setMessages([...messages, {'role': role, 'content':content, 'timestamp':timestamp}]);
    }

    return (
        <div className='tpp-chat-area'>
            <button className="tpp-toggle" onClick={taggleChatbox}>
                <span className="dashicons dashicons-format-chat"></span>
            </button>
            {showChat? (<div className="tpp-chatbox">
                <div className='tpp-chatbox-header'>
                    TPP - Virtual Agent
                </div>
                    <div className="tpp-chat-messages" ref={chatMessage} id='tpp-chat-msg'>
                        {messages.map((msg, index)=>{
                            if(msg.role=='calling'){
                                return ( <div className='clear' key={'msg-'+index}>
                                <div className="chatbot-container">
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                </div>
                                <div className='chat-timestamp'>
                                    <small>TPP</small>
                                </div>
                            </div>);
                            }else if(msg.role=='init'){
                                return (<div className="clear" key={'msg-'+index}>
                                {msg.items.map((item, index)=>{
                                    return (<div className="tpp-chat-message clear" key={'msg-item'+index}>
                                    {item}
                                </div>)
                                })}                            
                                <div className='chat-timestamp'>
                                    <small>{msg.timestamp}</small>
                                </div>
                            </div>);
                            }else {
                                return (<div className={"clear "+ (msg.role==="user"?"clear-user":"")} key={'msg-'+index}>
                                <div className={"tpp-chat-message "+ msg.role}>
                                    {msg.content}
                                </div>
                                <div className='chat-timestamp'>
                                    <small>{msg.timestamp}</small>
                                </div>
                            </div>);
                            }
                        }
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

export default Chatbot;