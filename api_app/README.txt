To encode the text :-

POST http://127.0.0.1:5000/encode/

Request Payload:

{
    "text":"Mississippi is known for its numerous double letters"
}

Response:

{
    "encoded_text": "11M4258+1i43467s29+p?11i12s?11k225n13o14w?11f12o13r?11i12t13s?11n227u13m14e15r16o18s?11d12o13u14b15l16e?11l225e234t16r17s"
}


To Decode the text :- 

POST http://127.0.0.1:5000/decode/

{
    "encoded_text": "11M4258+1i43467s29+p?11i12s?11k225n13o14w?11f12o13r?11i12t13s?11n227u13m14e15r16o18s?11d12o13u14b15l16e?11l225e234t16r17s"
}

Response:

{
    "decoded_text": "Mississippi is known for its numerous double letters"
}