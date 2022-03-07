# MakeOhio2022 - Ohio State Universities 24 Hour make-a-thon.
Software that detects driver inattention and puts vehicle in autopilot if the driver is incapacitated and unable to drive. <br />

**Honda Challenge**: Identify a condition(s) a driver may face and find a solution to increase user safety in vehicles. <br />
 <ul> 
  <li><i>Problem</i>: Most vehicle accidents are caused by distracted driving & many vehicle related deaths are caused by driver intoxication.</li>
  <li><i>Solution</i>: Developed a software that uses facial recognition to analyze the drivers current physical state and sends the appropriate response to car to increase safety</li>
  <ul>
    <li>If driver is distracted (Ex. texting), program uses speaker system to send pings to alert driver to focus on the road</li>
    <li>If driver is asleep at wheel, from intoxication or a medical emergency, program puts vehicle into autopilot which re aligns the vechile with the proper path of the road,             and slowly brings the car to a stop</li>
    <li>If multiple infractions of distracted driving, program automatically puts vechile into autopilot</li>
  </ul>
  <li>  <i>Process</i> : Built using Arduino and compatiable hardware</li>
 </ul>
 
 
 **Distracted Driving Recognition**
 <ul>
  <li> Used Python's Open CV library to develop facial regonition software that tracked and monitored eye movement</li>
  <li> Developed a tier system to determine weightage of infraction on result
  <ul>
    <li>If first infraction of distracted driving, <b>Warning 1</b> is sent</li>
    <li>If second infraction of distracted driving, <b>Warning 2</b> is sent</li>
    <li>If repeated infractions of distracted driving within time frame of 3 seconds, tier 3 <b>Autopilot</b> takes control of vehicle </li>
    <li>If driver is asleep or unresponsive at the wheel, tier 3 <b>Autopilot</b> takes control</li>.
  </ul>
 </ul>
