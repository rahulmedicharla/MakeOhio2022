# MakeOhio2022 - Ohio State University's 24 Hour make-a-thon.
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
 
 
 **Distracted Driving Recognition** -  Used Python's Open CV library to develop facial regonition software that tracked and monitored eye movement
 <ul>
  <li> Developed a tier system to determine weightage of infraction on result
  <ul>
    <li>If first infraction of distracted driving, <b>Warning 1</b> is sent</li>
    <li>If second infraction of distracted driving, <b>Warning 2</b> is sent</li>
    <li>If repeated infractions of distracted driving within time frame of 3 seconds, tier 3 <b>Autopilot</b> takes control of vehicle </li>
    <li>If driver is asleep or unresponsive at the wheel, tier 3 <b>Autopilot</b> takes control</li>.
  </ul>
 </ul>
 
 **Hardware** - Developed model car to test Autopilot on with Arduino
 <ul>
  <li>Warning 1: Send slow and quiet pings through arduino to small speaker to alert driver</li>
  <li>Warning 2: Send fast and loud pings through arduino to small speaker to alert driver</li>
 <li>Autopilot: Uses Arducam on arduino to find path to follow, corrects itself with refrence to that path with variable motor speeds, and then brings car to stop</li>
 <ul><li>Also turns on LED hazard lights to let surroundings vehicles know of the drivers condition.</li></ul>
 </ul>
 
 **Color Detection for Autopilot** - Used Python's Open CV library to do color detection on Arducam's feed and determine whether to turn left, turn right, or go straight
 FILL IN THE REST
