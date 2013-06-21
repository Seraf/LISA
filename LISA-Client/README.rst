The LISA-Client is a software which will be installed on multiple platforms.
This client will listen for a sound/voice and will transmit it to LISA-Engine.

As each platform can have his own speech to text software, the choice is your to select which engine to use.
If you're platform doesn't provide a compatible/usable engine, you can use the LISA-Speech software.

All sound will be streamed to LISA-Speech until the speech engine recognize the word "LISA".
Then, the client begin to record your sentence until the next silence (silence = stop to record).

It will send the sound to google to recognize, or use LISA-Speech (or any engine provided), get text from it, and send the text to LISA-Engine.
The client is also connected permanently to LISA-Engine. It allows to listen any event sent by the server like playing a sound or a sentence (to let LISA answer your question).

Clients can be multiple (one per room for example) if needed.
