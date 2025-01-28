import subprocess
import whisper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser
from gtts import gTTS
from moviepy import VideoFileClip
from pydub import AudioSegment
from dotenv import load_dotenv
import os
load_dotenv()
def extract_audio(ffmpeg_path, input_video, output_audio):
    """Extract audio from video using FFmpeg."""
    command = [
        ffmpeg_path,
        "-i", input_video,
        "-vn",  
        "-acodec", "pcm_s16le",  
        "-ar", "16000",  
        "-ac", "1",  
        output_audio
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path, model):
    """Transcribe audio to text using Whisper model."""
    result = model.transcribe(audio_path)
    return result["text"]

def translate_text_with_langchain(text, target_language):
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
    prompt_template = PromptTemplate(
        input_variables=["text", "target_language"],
        template="I want you to behave like a translator, translate the given text into the language {target_language} as if you are translating it in the real time to give it a look of a great translation:, dont explain anything or say any other thing than that\n\n{text} Use, !? In the sentence to make it speak with all emotions and the voice seems realistic"
    )
    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )
    translated_text = chain.invoke({'text':text, 'target_language':target_language})
    return translated_text['text']

def text_to_speech(text, language, output_audio_file):
    """Convert text to speech and save it as an audio file."""
    tts = gTTS(text=text, lang=language, slow=False)  
    tts.save(output_audio_file)
    print(f"Speech saved to {output_audio_file}")

def adjust_audio_speed(audio_file, original_video_path, output_file="adjusted_audio.mp3"):
    """Adjust the audio speed to match the video duration."""
    audio = AudioSegment.from_file(audio_file)
    video = VideoFileClip(original_video_path)
    target_duration = video.duration
    current_duration = audio.duration_seconds
    speed_factor = current_duration / target_duration
    adjusted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)
    adjusted_audio.export(output_file, format="mp3")
    return output_file

def replace_audio_in_video(ffmpeg_path, input_video, new_audio, output_video):
    """Replace the audio in the given video with the new audio file."""
    command = [
        ffmpeg_path,
        "-i", input_video,  # Input video
        "-i", new_audio,     # Input new audio
        "-c:v", "copy",      # Copy the video stream without re-encoding
        "-map", "0:v:0",     # Use the video stream from the first input
        "-map", "1:a:0",     # Use the audio stream from the second input
        "-shortest",         # Adjust to the shortest stream (video or audio)
        output_video         # Output file
    ]
    subprocess.run(command, check=True)
    print(f"New video saved to {output_video}")

def speech_to_speech_streaming(ffmpeg_path, input_video, target_language, output_audio_file, output_video_file):
    """Full pipeline: extract audio, transcribe, translate, and convert to speech."""
    
    # Step 1: Extract audio from video
    output_audio = "output_audio.wav"
    extract_audio(ffmpeg_path, input_video, output_audio)

    # Step 2: Transcribe audio to text using Whisper
    whisper_model = whisper.load_model("base")
    transcribed_text = transcribe_audio(output_audio, whisper_model)

    # Step 3: Translate the transcribed text using LangChain
    translated_text = translate_text_with_langchain(transcribed_text, target_language)

    # Step 4: Convert translated text to speech
    text_to_speech(translated_text, target_language, output_audio_file)

    # Step 5: Adjust audio speed to match video duration
    adjusted_audio_file = adjust_audio_speed(output_audio_file, input_video)

    # Step 6: Replace audio in the original video with the new translated audio
    replace_audio_in_video(ffmpeg_path, input_video, adjusted_audio_file, output_video_file)

if __name__ == "__main__":
    # Load OpenAI API key from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")

    # Paths
    ffmpeg_path = r"C:\Users\JMD\Downloads\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
    input_video = r"C:\Users\JMD\Desktop\Projects\speech_to_speech_streaming\input_video.mp4"
    target_language = 'hi' # Change to your desired target language
    output_audio_file = "translated_audio.mp3" 
    output_video_file = "output_with_new_audio.mp4"  

    # Run the speech-to-speech streaming pipeline
    speech_to_speech_streaming(ffmpeg_path, input_video, target_language, output_audio_file, output_video_file)
