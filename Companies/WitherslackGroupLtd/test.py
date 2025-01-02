import re

html_content = """
<h4><strong>Up to &pound;51,763 + Excellent benefits</strong></h4>

<h2>Please note: There is a potential opportunity for TLR with this position upon completion of probation.</h2>

<h4><strong>Those Huge Small Victories</strong></h4>

<p>Our teachers are fulfilled by the idea of making even the smallest positive changes in our young people, so we celebrate the little things. There&rsquo;s lots of ups and downs, and to some of our young people, sitting through a lesson can be a big win. We call these huge small victories and whilst they may seem small on the surface, they add up to make a big difference.</p>

<h2>&nbsp;</h2>

<h4><strong>Get out what you put in</strong></h4>

<p>You&rsquo;ll be working with children and young people with Autistic Spectrum Disorder/Social, Emotional and Mental Health needs. You&rsquo;ll be there to help them learn, develop their abilities and raise their self-esteem. You will need to be resilient and dedicated, but those huge small victories that you achieve will be something you&rsquo;re really proud of.</p>

<p>It can be a tough journey, but the positive steps forward will more than make up for it. As a Teacher at Witherslack Group, you&rsquo;ll get all the support you need to succeed, from in-house psychologists, to teaching assistants and therapy professionals. Your colleagues will be the best at what they do, the school environments will be well-resourced and we&rsquo;ll be with you every step of the way, helping you build a rewarding teaching career.</p>

<h4><strong>One of the best environments in SEND</strong></h4>

<p>Bescot Hall is a purpose built, brand new, state of the art school, catering primarily for children with Social, Emotional and Mental Health needs but also providing for children with autism who have moderate speech and learning needs. The school provides education for up to 72 children aged 8 to 16.</p>

<p>This new exciting opportunity serves Walsall and the wider communities, you are at the heart of its development. Our aim is to ensure that every pupil has an outstanding educational experience with individual pupil progress and care at the heart of what is offered.</p>

<h2>&nbsp;</h2>

<h4><strong>What we do for you</strong></h4>

<p>We know you&rsquo;re going to do great things. For your hard work and commitment, we reward you with the best salary and benefits package in the education sector. With us, you&rsquo;ll get to bring learning to life and make a genuine difference to the lives of our young people &ndash; plus you&rsquo;ll get:</p>

<ul>
	<li><strong>Training</strong>: A full induction and on the job training</li>
	<li><strong>Holiday</strong>: You&rsquo;ll work hard at WG, so you&rsquo;ll be rewarded with full school holidays</li>
	<li><strong>Progression</strong>: If career development is your thing, most of our head teachers and leaders have been promoted from within our group</li>
	<li><strong>Flexible benefits</strong>: meaning you can increase/decrease benefits such as life insurance &ndash; check out our benefits&nbsp;<a href="https://www.witherslackgroup.co.uk/careers/our-culture/benefits/" target="_blank">here</a></li>
	<li><strong>Pension:&nbsp;</strong>we offer a range of pensions to suit your lifestyle needs including Teachers&rsquo; Pension and our very attractive TPS alternative</li>
	<li><strong>Wellbeing: </strong>a host of wellbeing tools and advice including employee assistance</li>
	<li><strong>Medical cover</strong> so you can claim back the cost of things like an opticians or dentist appointment and a host of <strong>high-street discounts </strong></li>
	<li>
	<h4><strong>Beautiful working environments</strong> with the very best facilities &ndash; check out our schools&nbsp;<a href="https://www.witherslackgroup.co.uk/our-locations/our-schools/" target="_blank">here</a></h4>
	</li>
	<li>A recommend a friend scheme that offers a &pound;1,000 bonus every time</li>
</ul>

<h2>&nbsp;</h2>

<h2><strong>Bring your whole-self to work</strong></h2>

<p>Our young people come from all walks of life, diverse backgrounds and with different needs &ndash; and our workforce reflects that diversity, so that our teams can engage, encourage and inspire our young people to be themselves. You&rsquo;ll be more than aEnglish Teacher, you&rsquo;ll be able to connect with our pupils because of:</p>

<p>- Your &lsquo;can do&rsquo; attitude &ndash; a team player who rolls up their sleeves to help others- Your genuine passion for English and the impact your subject can have on young lives- The ability to relate your subject to each pupil and build great relationships with your class- Your enthusiasm and expertise to build your department- You&rsquo;ll also need previous teaching experience and have Qualified Teacher Status</p>

<h2>&nbsp;</h2>

<h4><strong>Interested in joining us?</strong></h4>

<p>Our young people deserve the best possible future and we feel the same about our teams. You deserve to have the career you want, with a purpose-led employer, in an environment that allows you to be yourself.</p>

<p><em>The Witherslack Group is committed to safeguarding and promoting the welfare of its young people. This post is subject to an enhanced DBS check (we will cover the cost) and an online search. We are an equal opportunities employer welcoming applications from all sections of the community.</em></p>

<p>For a full job description and person specification, please click <a href="http://witherslackgroup.box.com/s/dcwz268jsodctl1ycebpyffbc33dgrib" target="_blank">here.</a></p>

<p><em>To view our ex-offenders policy please click </em><a href="http://www.witherslackgroup.co.uk/media/dj3myptc/recruitment-of-ex-offenders-policy.pdf" target="_blank"><em>here</em></a><em>.</em></p>

<p>&nbsp;</p>

<p><em>To view our Child Protection Policy, please visit the &#39;Parents and Carers&#39; section of this School/Learning centre. You can find all our Schools </em><a href="http://gbr01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.witherslackgroup.co.uk%2Four-locations%2Four-schools%2F&amp;data=05%7C02%7CDaniel.Searle%40witherslackgroup.co.uk%7C2d85bd881215441904f208dcc7533876%7C32e69ada769447c18044b2f42b714fbb%7C0%7C0%7C638604407592223850%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&amp;sdata=%2BvX%2FMTT9qHN7IfLISh2s46sKkJKL80Qz7EmGo1Nd9e8%3D&amp;reserved=0" target="_blank"><em>here</em></a><em>.</em></p>

<p>Special Education / Careers in Care / Careers in Special Education / Working with Children / SEMH / SEN / ASD</p>

"""

# Replace <h2> or <h4> inside <li> with their content
html_content = re.sub(r'<br\s*/?>', '', html_content)
html_content = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', html_content)
html_content = re.sub(r'<h2><b>(.*?)</b></h2>', r'<h4><b>\1</b></h4>', html_content)
html_content = re.sub(r'<li>\s*<(h2|h4)>(.*?)</\1>\s*</li>', r'<li>\2</li>', html_content)
html_content = re.sub(r'<h2>(.*?)</h2>', r'<p>\1</p>', html_content)
empty_tag_pattern = r'<(p|span|div|li|b|i|strong|em)[^>]*>(\s*|&nbsp;|<span><span>&nbsp;</span></span>)</\1>'
html_content = re.sub(empty_tag_pattern, '', html_content)

print(html_content)
