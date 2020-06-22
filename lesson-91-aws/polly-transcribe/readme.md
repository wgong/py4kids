
## evaluate AWS Polly and Transcribe

1) download a text file from https://www.infoplease.com/primary-sources/government/presidential-speeches, e.g., Lincohn's famous Gettysburg address

2) use AWS Polly to convert text to speech using lang=en-US voice=Matthew
`$ python run_polly.py lincohn-gettysburg.txt Matthew `       

3) use AWS Transcribe to convert mp3 voice to text
`$ python run_transcribe.py lincohn-gettysburg-Matthew.mp3 `

4) Compare the original text with the transcribed text using cosine_similarity algorithm, 
we get a score of 0.9838, this suggests that AWS transcribe is pretty good.
`$ python compare_2text_files.py lincohn-gettysburg.txt lincohn-gettysburg-Matthew-tx.txt ` 


## References

- https://medium.com/@labrlearning/a-deep-dive-into-amazon-polly-3672baf6c624
- https://medium.com/@labrlearning/a-five-minute-overview-of-aws-transcribe-514b6cfeeddd


Note: 
```
processing time is 0:00:53.590105
transcript URL is https://s3.us-east-1.amazonaws.com/aws-transcribe-us-east-1-prod/578247465916/lincohn-gettysburg-Matthew/1ce6ea76-e0b1-42be-a211-6b5c6bcb168d/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQDW7eOpHBTTAxfeHjbd4ClxqVCQI8wERmfTl3Vv%2FUSTxgIgSZ%2Fni8ZBqwppVmZrtqq4%2BxKbhZ1%2FBSoJnJ9390lPwg8qtAMIUhABGgwyNzY2NTY0MzMxNTMiDIuXGo4gqaByP7eb6CqRA6AtysRDkyMKN%2Fpix2cP2D4ESRdcNm3sYU3ubuHRRnXGJqIusyV5I3dY2WQB0IrYLNhssxc75XVPrcAoF2mTa7ZHbThy9yJRr65ZlRyn4qXcTjqkwks9jNvcTbV8GPUwj5dlKtre5Fwexyt6IwNvbhCsSzFvgZKLLyqfAqqeexBDrqUXi0qVWwpX1AdEOyPOrrfnFbd89KPRy%2ByHMdq%2BY%2FF%2Fpd5mwVm%2FG9Kko6DaaIhxSfxvnx9%2Blb8B1zmYJuONF3if%2BZMNrIBnkuxx7lgww8h6TmU8RkIdus90MMOOgwdyv1TMzhCdLUtzSeLPPINfZlTz7RojhWm0cTfoQP7IVA%2BGXKkXS280y2ZhTC0GSU7piYCwXaDE9deOWPbgq7%2FSfSfUUynaTgsCaJ%2BDiVwcVYdFyiF8JQzUMfWZtRVawaJTpjMfst9sCWVx8DZh8piv87xN8sCt8Rjugu99jSUTh0sJ8rxcjq32W8xm9VXKtLRiKzHbzIU%2FSZfdpGtX45q5ewGQ0RIGHy0WYp8qsFfKxG4PMO6JwPcFOusBjnRr1Z3fNICErCLhjZMXr%2BJGY1okjDJhQtPWuyQERXhrbwB3yA%2Bepesn34MDp8mHyU%2BEfir2Vby%2FIJvz09s1NkvDD%2F90D6IZ5d%2FW2fU98nm%2B4FQ6q4ryNafhgGBvimKg5nhz93AIz9WBRyXBspBOozrUhk6EPKjgCZj17wWq6LievnO4Orc0YdxvhMYUa8nIx%2FFaMB%2F05Svjtkhbg8Ppk8jwzawW3kkpTgB3Lu1804i%2BkEu5p%2BN%2FSXC3d%2BdGQzUXJVjf0Z27tKeGYaY20qMBhmo7%2FMJyTOXEZXDJoi4Md6HOSRzQsUmneQpz6w%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200622T021223Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=ASIAUA2QCFAA3BWU7K2P%2F20200622%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=7b267495bc7869e765569da2f12aeea4cb1f5256dfde0636f56fa881f8825340
```