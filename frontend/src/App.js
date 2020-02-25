import React, { useState, useEffect } from 'react';
import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl'

function App() {

    const [image, setImage] = useState(null);
    const [scores, setScores] = useState(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState(null);

    const onClick = (event) => {
        event.preventDefault();
        const formData = new FormData();

        
        console.log(image);

        fetch("http://localhost:8000/predict", {
          method: 'POST',
          body: image,
          headers: {'Content-Type': 'application/json'}
        })
        .then(res => res.json())
        .then(scores => {
          setScores(scores.values)

        })
        
    }

    const onImageChange = (event) => {
        event.preventDefault();

        let reader = new FileReader();
        let file = event.target.files[0];

        reader.onloadend = (e) => {
            var data = e.target.result.replace("data:"+ file.type +";base64,", '');
            setImage(data);
            setImagePreviewUrl(reader.result);
        }

        reader.readAsDataURL(file)
    }

    let img = null;
    let scrs = null;

    if (imagePreviewUrl !== null) {
        img = <img src={imagePreviewUrl}/>;
    }

    if (scores !== null) {
        scrs = <ul>{scores.map((score, index) => <li className={index===0?"bold":""} key={index}>{score.label}:{score.score}</li>)}</ul>
    }

  return (
    <Form>
      <InputGroup className="mb-3">
      <Button onClick={onClick} variant="primary" type="submit">
        Submit
      </Button>
      <FormControl
          onChange={onImageChange}
        type="file" 
      />
       
    </InputGroup>
    {img}
    {scrs}
    </Form>
  );
}

export default App;
