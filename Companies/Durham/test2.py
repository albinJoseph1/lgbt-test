import re

html_content = '''
<p>Disclosure and Barring Service Requirement:&nbsp;Not Applicable.&nbsp;</p>

<p><strong>Working at Durham University&nbsp;&nbsp;</strong></p>

<p>A globally outstanding centre of teaching and research excellence, a warm and friendly place to work, a unique and historic setting &ndash; Durham is a university like no other.</p>

<p>As one of the UK&rsquo;s leading universities, Durham is an incredible place to define your career. The University is located within a beautiful historic city, home to a UNESCO World Heritage Site, and surrounded by stunning countryside. Our talented scholars and researchers from around the world are tackling global issues and making a difference to people&#39;s lives.&nbsp;&nbsp;</p>

<p>We believe that inspiring our people to do outstanding things at Durham enables Durham people to do outstanding things in the world. Being a part of Durham is about more than just the success of the University, it&rsquo;s also about contributing to the success of the city, county and community.</p>

<p>Our University Strategy is built on three pillars of research, education and wider student experience, but also on our keen sense of community and of inspiring others to achieve their potential.&nbsp;</p>

<p><strong>Our Purpose and Values</strong></p>

<p>We want our University to be a place where people can be free to be themselves, no matter what their identity or background. Together, we celebrate difference, value one another and are each responsible for creating an inclusive community that is respectful and fair for all.</p>

<p>Find out more about the benefits of working at the University and what it is like to live and work in the Durham area on our&nbsp;Why Join Us? - Information Page</p>

<p>A competitive salary is only one part of the many fantastic benefits you will receive if you join the University: you will also receive access to the following fantastic benefits:</p>

<p>&bull; 30 Days annual leave per year in addition to 8 public holidays and 4 customary days per year &ndash; a total of 42 days per year.&nbsp;</p>

<p>&bull; The University closes between Christmas and New Year &ndash; please include or delete if not applicable.</p>

<p>&bull; We offer a generous pension scheme, as a new member of staff you will be automatically enrolled into the University Superannuation Scheme (USS).</p>

<p>&bull; No matter how you travel to work, we have you covered. We have parking across campus, a cycle to work scheme which helps you to buy a bike and discount with local bus and train companies.</p>

<p>&bull; There is a genuine commitment to developing our colleagues professionally and personally. There is a comprehensive range of development courses, apprenticeships and access to qualifications and routes to develop your career in the University. All staff have dedicated annual time to concentrate on their personal development opportunities.</p>

<p>&bull; Lots of support for health and wellbeing including discounted membership for our state-of-the-art sport and gym facilities and access to a 24-7 Employee Assistance Programme.</p>

<p>&bull; On site nursery is available and children&rsquo;s clubs in the summer holidays.</p>

<p>&bull; Family friendly policies, including maternity and adoption leave, which are among the most generous in the higher education sector (and likely above and beyond many employers).</p>

<p>&bull; The opportunity to take part in staff volunteering activities to make a difference in the local community</p>

<p>&bull; Discounts are available via our benefits portal including money off at supermarkets, high street retailers, IT products such as Apple, the cinema and days out at various attractions.</p>

<p>&bull; A salary sacrifice scheme is also available to help you take advantage of tax savings on benefits.</p>

<p>&bull; If you are moving to Durham, we can help with removal costs and we have a dedicated team who can help you with the practicalities such as house hunting and schools. If you need a visa, we cover most visa costs and offer an interest free loan scheme to pay for dependant visas.</p>

<p><span style="color:#000000"><strong>The Department</strong></span></p>

<p><span style="color:#000000">The Centre for Advanced Instrumentation (CfAI) is a large research group in the Department of Physics at Durham University with approximately seventy staff and research students. CfAI&rsquo;s mission is to design and develop novel instrumentation based on cutting edge technologies. CfAI develops state-of-the-art ground and space-based instruments for applications across a wide range of disciplines including adaptive optics, spectroscopy, biophysics, remote sensing, laser communications, and fusion diagnostics. </span></p>

<p><span style="color:#000000">The centre is currently involved in various laser communications projects, including a world first demonstration of the use of laser guide stars for laser communications, and in modelling and forecasting the turbulence at potential optical ground station sites. CfAI is further expanding its reach in to the fields of free space optical communications, space surveillance and earth observation through the creation of a new interdisciplinary &ldquo;Space Research Centre&rdquo; (SPARC). </span></p>

<p><span style="color:#000000"><strong>The Role</strong></span></p>

<p><span style="color:#000000">Applications are invited for a Postdoctoral Research Associate position in the Space Research group in Durham. The role will be focused on the development and modelling of adaptive optics systems for the application of free space optical communications. The role is initially funded by the newly instituted &ldquo;Space Research Centre&rdquo; (SPARC), and collaborative work with other departments in the centre will be performed. </span></p>

<p><span style="color:#000000">The position will be centred on adaptive optics systems and laser guide stars for Free Space Optical Communication (FSOC) with satellites. This includes modelling so called &ldquo;Strong Turbulence&rdquo; conditions experienced during low elevation satellite links through computer simulation and laboratory experiments. There is a longer term goal of demonstrating the technologies in links through real turbulence with test sources or even real satellites. Further examination of the use of Laser Guide Stars in FSOC will also be performed, leveraging the CfAI&rsquo;s previous expertise on the topic.</span></p>

<p><span style="color:red"><span style="color:#000000">Through this position you will be making a crucial contribution to the development of this international astronomy facility, and the demonstration of an exciting new technology. This role will suit someone who wishes to gain practical experience of taking novel research outputs and developing technologies from them to the level where they can be incorporated into cutting edge scientific instruments. You will be expected to work in close collaboration with other members of CfAI and SPARC as well as our international partners who have a wide range of scientific and engineering backgrounds.</span> </span></p>

<p><strong>Responsibilities:</strong></p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To understand and convey material of a specialist or highly technical nature to the team or group of people through presentations and discussions that leads to the presentation of research papers in conferences, project design reviews and publications.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To prepare and deliver presentations on research outputs/activities to audiences which may include: research sponsors, academic and non-academic audiences.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To publish high quality outputs, including papers for submission to peer reviewed journals and papers for presentation at conferences and workshops under the direction of the Principal Investigator or Grant-holder.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To assist with the development of research objectives and proposals.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To conduct individual and collaborative research projects under the direction of the Principal Investigator or Grant-holder.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To work with the Principal Investigator or Grant-holder and other colleagues in the research group, as appropriate, to identify areas for research, develop new research methods and extend the research portfolio.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To deal with problems that may affect the achievement of research objectives and deadlines by discussing with the Principal Investigator or Grant-holder and offering creative or innovative solutions.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To liaise with research colleagues and make internal and external contacts to develop knowledge and understanding to form relationships for future research collaboration.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To plan and manage own research activity, research resources in collaboration with others and contribute to the planning of research projects.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To deliver training in research techniques/approaches to peers, visitors and students as appropriate.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To be involved in student supervision, as appropriate, and assist with the assessment of the knowledge of students.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To contribute to fostering a collegial and respectful working environment which is inclusive and welcoming and where everyone is treated fairly with dignity and respect.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To engage in wider citizenship to support the department and wider discipline.</p>

<p>&bull;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To engage in continuing professional development by participation in the undergraduate or postgraduate teaching programmes or by membership of departmental committees, etc. and by attending relevant training and development courses.&nbsp;&nbsp;&nbsp;</p>

<p><span style="color:#000000">This post is fixed term for 2 years to coincide with the duration of our existing funding, with the possibility for extension. </span></p>

<p><span style="color:#000000">The post-holder is employed to work on a research project which will be led by another colleague. Whilst this means that the post-holder will not be carrying out independent research in his/her own right, the expectation is that they will contribute to the advancement of the project, through the development of their own research ideas/adaptation and development of research protocols.</span></p>

<p><span style="color:#000000">Successful applicants will, ideally, be in post by 1st January 2025.</span></p>

<div style="margin-left:0; margin-right:0">
<p style="margin-left:0; margin-right:0"><strong>Durham University is committed to equality, diversity and inclusion</strong></p>
</div>

<div style="margin-left:0; margin-right:0">
<p style="margin-left:0; margin-right:0">Equality, diversity, and inclusion (EDI) are a key component of the University&rsquo;s Strategy <span style="background-color:#ffffff">and a central part of everything we do.  We also live by our </span><a class="Hyperlink SCXW95353610 BCX8" href="https://www.dur.ac.uk/about/values/" rel="noreferrer noopener" style="-webkit-user-drag: none; -webkit-tap-highlight-color: transparent; margin: 0px; padding: 0px; user-select: text; cursor: text; text-decoration: none; color: inherit;" target="_blank"><u>Purpose and Values</u></a><span style="background-color:#ffffff"> and our </span><a class="Hyperlink SCXW95353610 BCX8" href="https://www.durham.ac.uk/media/durham-university/professional-services/job-vacancies/job-descriptions/STAFF-CODE-OF-CONDUCT.pdf" rel="noreferrer noopener" style="-webkit-user-drag: none; -webkit-tap-highlight-color: transparent; margin: 0px; padding: 0px; user-select: text; cursor: text; text-decoration: none; color: inherit;" target="_blank"><u>Staff Code of Conduct.</u></a><span style="background-color:#ffffff">  At Durham we actively work towards providing an environment where our staff and students can study, work and live in a community which is supportive and inclusive. It&rsquo;s important to us that all colleagues undertake activities that are aligned to both our values and commitment to EDI. </span>&nbsp;</p>
</div>

<div style="margin-left:0; margin-right:0">
<p style="margin-left:0; margin-right:0">We welcome and encourage applications from those who are currently under-represented in our work force, including people with disabilities and from racially minoritised ethnic groups. &nbsp;</p>
</div>

<div style="margin-left:0; margin-right:0">
<p style="margin-left:0; margin-right:0"><span style="background-color:#ffffff">If you have taken a career break or periods of leave that may have impacted on the volume and recency of your research outputs and other activities, such as maternity, adoption or parental leave, you may wish to disclose this in your application. The selection committee will take this into account when evaluating your application.&nbsp;</span>&nbsp;</p>
</div>

<div style="margin-left:0; margin-right:0">
<p style="margin-left:0; margin-right:0"><span style="background-color:#ffffff">The University has been awarded the Disability Confident Employer status. If you are a candidate with a disability, we are committed to ensuring fair treatment throughout the recruitment process. We will make adjustments to support the interview process wherever it is reasonable to do so and, where successful, reasonable adjustments will be made to support people within their role. </span>&nbsp;</p>
</div>
'''

# pattern = r'&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.*?)(?=&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|</)'
# result = re.sub(pattern, r'<ul><li>\1</li></ul>', html_content)
# empty_tag_pattern = r'<\s*\w+[^>]*>\s*(?:&nbsp;|\s)*</\s*\w+>'
# html_content = re.sub(empty_tag_pattern, '', result)
# nbsp_pattern = r'(&nbsp;\s*)\1+'
# html_content = re.sub(nbsp_pattern, r'&nbsp;', html_content)



html_content = re.sub(r'style="[^"]*"', '', html_content)
empty_tag_pattern = r'<(\w+)(\s+[^>]*)?>\s*(<\w+>\s*</\w+>\s*)*\s*</\1>'
html_content = re.sub(empty_tag_pattern, '', html_content)
pattern = r'&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.*?)(?=&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|</)'
pattern = r'(&middot;|&bull;)(.*?)(?=&(?:middot;|bull;)|</|<br)'

result = re.sub(pattern, r'<ul><li>\1</li></ul>', html_content)
empty_tag_pattern = r'<\s*\w+[^>]*>\s*(?:&nbsp;|\s)*</\s*\w+>'
html_content = re.sub(empty_tag_pattern, '', result)
nbsp_pattern = r'(&nbsp;\s*)\1+'
html_content = re.sub(nbsp_pattern, r'&nbsp;', html_content)


# html_content = re.sub(r'style="[^"]*"', '', html_content)

# # Remove empty tags (tags that contain only other empty tags or whitespace)
# empty_tag_pattern = r'<(\w+)(\s+[^>]*)?>\s*(<\w+>\s*</\w+>\s*)*\s*</\1>'
# html_content = re.sub(empty_tag_pattern, '', html_content)

# # Updated pattern to match &middot; or &bull; followed by &nbsp; and text
# pattern = r'(&bull;|&middot;)(\s*&nbsp;\s*)*(.*?)(?=&bull;&nbsp;|&middot;&nbsp;|</)'
# result = re.sub(pattern, r'<ul><li>\3</li></ul>', html_content)

# # Remove empty tags (similar to above) for leftover content
# empty_tag_pattern = r'<\s*\w+[^>]*>\s*(?:&nbsp;|\s)*</\s*\w+>'
# html_content = re.sub(empty_tag_pattern, '', result)

# # Handle consecutive &nbsp; by replacing them with a single &nbsp;
# nbsp_pattern = r'(&nbsp;\s*)\1+'
# html_content = re.sub(nbsp_pattern, r'&nbsp;', html_content)


print(html_content)
