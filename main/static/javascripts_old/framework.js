function Circle( x,y,size,color )
{
	context.fillStyle = color;
	context.beginPath();
	context.arc( x,y,size,0,2 * Math.PI );
	context.fill();
}

function FindAngle ( x0,y0,x1,y1 )
{
	const delta_x = x1 - x0;
	const delta_y = y1 - y0;
	var theta = Math.atan2( delta_y,delta_x );
	theta *= ( 180 / Math.PI );
	return theta;
}

function FindDistance ( x0,y0,x1,y1 )
{
	const delta_x = x1 - x0;
	const delta_y = y1 - y0;
	const distance = Math.sqrt( ( delta_x * delta_x ) + ( delta_y * delta_y ) );
	return distance;
}

function HitTest( x0,y0,w0,h0,x1,y1,w1,h1 )
{
	if( x0 < x1 + w1 && x0 + w0 > x1 &&
		y0 < y1 + h1 && y0 + h0 > y1)
	{
		return true;
	}
	else
	{
		return false;
	}
}

function Random( min,max )
{
	if( min > max )
	{
		const temp = max;
		max = min;
		min = temp;
	}
	const randomNumber = Math.floor( Math.random() * ( 1 + max - min ) ) + min;
	return randomNumber;
}

function Rect( x,y,width,height,color,alpha = 1.0 )
{
	if( alpha === 1.0 )
	{
		context.fillStyle = color;
		context.fillRect( x,y,width,height );
	}
	else
	{
		context.globalAlpha = alpha;
		context.fillStyle = color;
		context.fillRect( x,y,width,height );
		context.globalAlpha = 1.0;
	}
}

function Text( x,y,message,color,font = "20PX Arial" )
{
	context.fillStyle = color;
	context.font = font;
	context.fillText( message,x,y );
}