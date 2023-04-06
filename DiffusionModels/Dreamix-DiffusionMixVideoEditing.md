# Dreamix: Video Diffusion Models are General Video Editors 

Text-driven image and video diffusion models have recently achieved unprecedented generation realism. While diffusion models have been successfully applied for image editing, very few works have done so for video editing. We present the first diffusion-based method that is able to perform text-based motion and appearance editing of general videos. Our approach uses a video diffusion model to combine, at inference time, the low-resolution spatio-temporal information from the original video with new, high resolution information that it synthesized to align with the guiding text-prompt. As obtaining high-fidelity to the original video requires retaining some of its high-resolution information, we add a preliminary stage of finetuning the model on the original video, significantly boosting fidelity. We propose to improve motion editability by a new, mixed objective that jointly finetunes with full temporal attention and with temporal attention masking. We further introduce a new framework for image animation. We first transform the image into a coarse video by simple image processing operations such as replication and perspective geometric projections, and then use our general video editor to animate it. As a further application, we can use our method for subject-driven video generation. Extensive qualitative and numerical experiments showcase the remarkable editing ability of our method and establish its superior performance compared to baseline methods.

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp; Dreamix - Applying Video Diffusion Models as General Video Editors (AI-fused Video Editing)</b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![Dreamix - Applying Video Diffusion Models as General Video Editors (AI-fused Video Editing)](https://img.youtube.com/vi/lDuYegL4DyQ/0.jpg)](https://www.youtube.com/watch?v=lDuYegL4DyQ)

  </tr>
</table>

  
## Resources:
- https://dreamix-video-editing.github.io/
- https://github.com/nateraw/stable-diffusion-videos

